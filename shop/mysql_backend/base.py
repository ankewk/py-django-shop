"""
自定义 MySQL 后端基础类，支持 MySQL 5.7
"""

from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper
from django.db.backends.mysql.base import DatabaseFeatures as MySQLDatabaseFeatures
from django.db.backends.mysql.base import DatabaseOperations as MySQLDatabaseOperations
from django.db.backends.mysql.base import DatabaseClient as MySQLDatabaseClient
from django.db.backends.mysql.base import DatabaseCreation as MySQLDatabaseCreation
from django.db.backends.mysql.base import DatabaseIntrospection as MySQLDatabaseIntrospection
from django.db.backends.mysql.base import DatabaseValidation as MySQLDatabaseValidation

class DatabaseFeatures(MySQLDatabaseFeatures):
    """MySQL 5.7 兼容的特性"""
    
    def __init__(self, connection):
        super().__init__(connection)
        # 禁用 MySQL 8.0 特定功能
        self.supports_expression_indexes = False

class DatabaseOperations(MySQLDatabaseOperations):
    """MySQL 5.7 兼容的操作"""
    pass

class DatabaseClient(MySQLDatabaseClient):
    """MySQL 5.7 兼容的客户端"""
    pass

class DatabaseCreation(MySQLDatabaseCreation):
    """MySQL 5.7 兼容的数据库创建"""
    pass

class DatabaseIntrospection(MySQLDatabaseIntrospection):
    """MySQL 5.7 兼容的数据库内省"""
    pass

class DatabaseValidation(MySQLDatabaseValidation):
    """MySQL 5.7 兼容的数据库验证"""
    pass

class DatabaseWrapper(MySQLDatabaseWrapper):
    """自定义 MySQL 数据库包装器"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.features = DatabaseFeatures(self)
        self.ops = DatabaseOperations(self)
        self.client = DatabaseClient(self)
        self.creation = DatabaseCreation(self)
        self.introspection = DatabaseIntrospection(self)
        self.validation = DatabaseValidation(self)
    
    def check_database_version_supported(self):
        """重写版本检查，支持 MySQL 5.7"""
        # 跳过版本检查
        pass 