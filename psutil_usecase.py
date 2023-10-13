def redis_daemon_exist():
    # We can just check of 'redis-server' process because the default
    # situation is that we are in a container without any other python2
    # process.
    import psutil

    pids = psutil.pids()
    process_names = []

    for pid in pids:
        try:
            name = psutil.Process(pid).name()
        except psutil.NoSuchProcess:
            name = None
        process_names.append(name)

    return "redis-server" in process_names


redis_daemon_exist()
