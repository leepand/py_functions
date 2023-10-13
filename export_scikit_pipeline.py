import json


def fullname(o):
    return o.__module__ + "." + o.__class__.__name__


def export_pipeline(scikit_pipeline):
    """JSON export of a scikit-learn pipeline.

    Especially useful when paired with GridSearchCV, TPOT, etc.

    Example:
    best_model = GridSearchCV(
        some_pipeline,
        param_grid=some_tuning_parameters
    )
    best_model.fit(X=train_x, y=train_y)
    export_pipeline(best_model.best_estimator_)
    :param scikit_pipeline: a scikit-learn Pipeline object
    """
    steps_obj = {"steps": []}
    for name, md in scikit_pipeline.steps:
        steps_obj["steps"].append(
            {"name": name, "class_name": fullname(md), "params": md.get_params()}
        )

    return steps_obj
