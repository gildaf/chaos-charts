import redis


class RaftClient(redis.RedisCluster):

    def raft_info(self, target_nodes=None):
        """
        :param target_nodes: can take the same type as `execute_command` in `redis.Cluster`
        https://github.com/redis/redis-py#getting-started
        """
        lines = self.execute_command("INFO raft", target_nodes=target_nodes).strip().split("\n")
        return dict([line.strip().split(":") for line in lines if not line.startswith("#") and ":" in line])

    def is_up(self) -> bool:
        info = self.raft_info(target_nodes=self.PRIMARIES)
        return info['raft_state'] == 'up'
