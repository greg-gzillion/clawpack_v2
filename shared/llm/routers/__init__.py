"""Router Factory"""
from .base import BaseRouter
from .priority import PriorityRouter
from .round_robin import RoundRobinRouter
from .smart import SmartRouter

class RouterFactory:
    @staticmethod
    def create(router_type: str = "priority", **kwargs) -> BaseRouter:
        routers = {
            "priority": PriorityRouter,
            "round_robin": RoundRobinRouter,
            "smart": SmartRouter
        }
        router_class = routers.get(router_type, PriorityRouter)
        return router_class(**kwargs)
