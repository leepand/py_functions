#%%file e_test.py
import xgboost
import pickle
import json
import redis
from get_feats import get_context_features
import fastapi
from modelkit import Model, ModelLibrary
from modelkit.api import ModelkitAutoAPIRouter

from modelkit.core.model import AsyncModel, Model, WrappedAsyncModel

# from gevent import Greenlet
import threading

# import gevent.monkey
# gevent.monkey.patch_all()


r_server_a = redis.StrictRedis(host="xx.com", port=6379, db=10)


def load_obj(path):
    with open(path, "rb") as f:
        obj = pickle.load(f)
    return obj


_model = load_obj("model.pkl")
transformer = load_obj("transformer.pkl")


class myThread(threading.Thread):
    def __init__(
        self,
        threadID,
        uid,
        async_user_id,
        async_experiment_sequence_id,
        async_strategy_sequence_id,
        async_server_id,
    ):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.uid = uid
        self.async_user_id = async_user_id
        self.async_experiment_sequence_id = async_experiment_sequence_id
        self.async_strategy_sequence_id = async_strategy_sequence_id
        self.async_server_id = async_server_id

    def run(self):
        # print ("开启线程： " + self.uid)
        # 获取锁，用于线程同步
        threadLock = threading.Lock()
        threadLock.acquire()
        predict_churn22(
            self.uid,
            self.async_user_id,
            self.async_experiment_sequence_id,
            self.async_strategy_sequence_id,
            self.async_server_id,
        )
        # 释放锁，开启下一个线程
        threadLock.release()


def predict_churn22(
    uid,
    async_user_id,
    async_experiment_sequence_id,
    async_strategy_sequence_id,
    async_server_id,
):
    status = "ok"
    try:
        df = get_context_features(uid)
        X = transformer.transform(df)
        predicted_churn = _model.predict(X)[0]
        predicted_proba_churn = _model.predict_proba(X)[0][1]
    except:
        status = "error"
        predicted_churn = 0
    # print(predicted_churn,"predicted_churn")
    msg = {
        "result": {"status": status, "predicted_churn": str(predicted_churn)},
        "async_user_id": async_user_id,
        "async_experiment_sequence_id": async_experiment_sequence_id,
        "async_strategy_sequence_id": async_strategy_sequence_id,
    }

    channel = "server:{}".format(async_server_id)
    # print(msg,"json.dumps(msg)")
    r_server_a.publish(channel, json.dumps(msg))

    # return predicted_churn
    # print({"predicted_churn": str(predicted_churn),
    #               "predicted_proba_churn": str(predicted_proba_churn)})


class onlinePredictChurn(Model):
    CONFIGURATIONS = {"onlinepredictchurn": {}}

    def _predict(self, items):
        uid = items.get("async_user_id")
        async_user_id = uid
        async_server_id = items.get("async_server_id")
        async_experiment_sequence_id = items.get("async_experiment_sequence_id")
        async_strategy_sequence_id = items.get("async_strategy_sequence_id")
        # 创建新线程
        thread1 = myThread(
            1,
            uid,
            async_user_id,
            async_experiment_sequence_id,
            async_strategy_sequence_id,
            async_server_id,
        )
        # 开启新线程
        thread1.start()

        # g = Greenlet.spawn(predict_churn22,
        #                   uid,
        #                   async_user_id,
        #                   async_experiment_sequence_id,
        #                   async_strategy_sequence_id,
        #                   async_server_id)

        return {"status": "ok"}


# predict("16620926")

# Create the model library
library = ModelLibrary(models=[onlinePredictChurn])

# Get the model

model = library.get("onlinepredictchurn")


app = fastapi.FastAPI()
router = ModelkitAutoAPIRouter(
    required_models=["onlinepredictchurn"], models=[onlinePredictChurn]
)
app.include_router(router)

data = {
    "async_user_id": "6674637",
    "async_server_id": "16509136_1",
    "async_experiment_sequence_id": "10",
    "async_strategy_sequence_id": "10",
    "result": {"status": "ok", "predicted_churn": "predicted_churn"},
}

model(data)


import redis

r_server_a = redis.StrictRedis(host="xx.com", port=6379, db=10)

async_server_id = 7
channel = "server:{}".format(async_server_id)
pubsub = r_server_a.pubsub()
pubsub.subscribe(channel)

for item in pubsub.listen():
    print(item)
