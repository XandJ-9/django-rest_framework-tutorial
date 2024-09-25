'''
对不同的对象选择不同的数据库进行操作
'''


class AuthRouter:
    """
    自动路由
    """
    router_app_labels={"auth","contenttypes"}

    def db_for_read(self, model, **hints):
        """
        只读操作路由到从库
        """
        if model._meta.app_label in self.router_app_labels:
            return 'drf_auth'
        return None

    def db_for_write(self, model, **hints):
        """
        写操作路由到主库
        """
        if model._meta.app_label in self.router_app_labels:
            return 'drf_auth'
        return None

    def allow_relation(self, obj1, obj2,**hints):
        """
        关联对象之间的操作
        """
        if (
            obj1._meta.app_label in self.router_app_labels
            or obj2._meta.app_label in self.router_app_labels
        ):
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        默认所有操作都路由到主库
        """
        if app_label in self.router_app_labels:
            return db == 'drf_auth'
        return None
    

class SysRouter:
    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly-chosen replica.
        """
        # return random.choice(["replica1", "replica2"])
        return "drf_system"

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        return "drf_system"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the primary/replica pool.
        """
        db_set = {"drf_system", "replica1", "replica2"}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        if db == "drf_system" and app_label == "myapp.system":
            return True
        return True