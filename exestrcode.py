code = "print('hahahaha');print('sdsd')"
import builtins
import numpy
import numpy as np

safe_builtins = builtins.__dict__.copy()

safe_builtins.update({"numpy": np, "np": np})
byte_code = compile(code, filename="<inline code>", mode="exec")
exec(byte_code, {"__builtins__": safe_builtins})
