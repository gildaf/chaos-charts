import redis


def _info_callback(_command, response, **kwargs):
    """
    Usually the cluster client returns a result with a
    structure of {<node_name1>: <some value 1>, <node_name2>: <some value 2>}
    But, if there is only one element in the result dict it will just return <some value>.
    see https://github.com/redis/redis-py/blob/fcd8f98509c5c7c14ee5a3201b56b8bf755a4b7c/redis/cluster.py#L1198
    This means that when we send execute_command("INFO", target_nodes=PRIMARIES) we cant know if the dict we got
    is just single info response or a response from multiple nodes.
    By adding a callback we are bypassing this behavior, so we always get back a dict
    with {<node_name1>: <some value 1>, <node_name2>: <some value 2>}
    """
    return response


class RaftClient(redis.RedisCluster):

    def __init__(self, **kwargs):
        super(RaftClient, self).__init__(**kwargs)
        self.result_callbacks["INFO"] = _info_callback

    def raft_info(self, target_nodes=None):
        """
        :param target_nodes: can take the same type as `execute_command` in `redis.Cluster`
        https://github.com/redis/redis-py#getting-started
        INFO has a strange api
        """
        return self.execute_command("INFO", "raft", target_nodes=target_nodes)

    def assert_raft_is_up(self):
        infos = self.raft_info(target_nodes=self.PRIMARIES)
        for host, info in infos.items():
            if info['raft_state'] != 'up':
                raise Exception(f"Node {host} is not up")

