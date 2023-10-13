from ab_client import participate, convert

# 正常分组，第一个参数：实验名称，第二个参数：实验组list，第三个参数client_id（同一个id只曝光一次）

participate("test_ab", ["test", "control"], client_id="001")
"""
response:

{'status': 'ok',
 'alternative': {'name': 'control'},
 'experiment': {'name': 'test_ab'},
 'request_id': '001'}
 """
# 反馈：通过kpi参数指定转化指标（如CVR），同一个流量可以复用，即制定不同的kpi，前端可以看到不同转化指标的转化情况
convert("test_ab", client_id="001", kpi="CVR")

# 特殊分组：如果需要将某个client_id(request_id) 强制分到某个组，且记录曝光（record_force=True，默认只分组不曝光）
participate(
    "test_ab", ["test", "control"], client_id="002", force="test", record_force=True
)
