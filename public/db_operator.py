import pymysql
from dbutils.pooled_db import PooledDB
import sys
sys.path.append('..')
import conf
# import log.custom_logger as custom_logger

class DBOperator:
	# 数据库的基础操作，增删改查，
	# 使用数据库池以支持多线程操作
	
	def __init__(self):
		pass

	def database_config(self, db_name):
		# 数据库的配置
		# 输入：
		# db_name：数据库名称

		return PooledDB(
			creator=pymysql,  # 使用链接数据库的模块
			maxconnections=None,  # 连接池允许的最大连接数，0和None表示不限制连接数
			mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
			maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
			maxshared=1,
			# 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
			blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
			maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
			setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
			ping=0,
			# ping MySQL服务端，检查是否服务可用。
			# 如：0 = None = never,
			# 1 = default = whenever it is requested,
			# 2 = when a cursor is created,
			# 4 = when a query is executed,
			# 7 = always
			host=conf.db_host,
			port=conf.db_port,
			user=conf.db_user,
			password=conf.db_password,
			database=db_name,
			charset='utf8'
		)
	
	def create_conn(self, db_name):
		# db_name：创建哪个模块的数据库连接池
		# 来自 db_config.py 的 DATABASES
		
		# 创建数据库连接池
		# 输出：与数据库的链接，数据库操作游标
		
		# 连接数据库
		conn = self.database_config(db_name).connection()
		# 数据库操作游标
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		return conn, cursor


	def close_conn(self, conn, cursor):
		# conn：数据库的链接
		# cursor：数据库操作游标
		
		# 关闭数据库链接和操作游标
		# 需按顺序，先关 操作游标，再关数据库链接
		cursor.close()
		conn.close()
	
	
	def select_one(self, db_name, sql):
		# db_name：创建哪个模块的数据库连接池
		# sql: 需要插入数据库的sql query
		# 查一个
		# 输出： 返回查询结果
		
		# 创建链接和操作游标
		conn, cur = self.create_conn(db_name)
		try:
			# 如果数据库连接失败，则重连
			conn.ping(reconnect=True)
			# 执行sql语句
			cur.execute(sql)
			# 获取结果
			result = cur.fetchone()
			# 关闭
			self.close_conn(conn, cur)
			# 返回查询结果
			return result
			
		except Exception as e:
			# 如果发生错误则回滚
			conn.rollback()
			print(e)
			# 关闭
			self.close_conn(conn, cur)
			


	def select_all(self, db_name,sql):
		# db_name：创建哪个模块的数据库连接池
		# sql: 需要插入数据库的sql query
		# 查全部
		# 输出： 返回查询结果
		
		# 创建链接和操作游标
		conn, cur = self.create_conn(db_name)
		try:
			# 如果数据库连接失败，则重连
			conn.ping(reconnect=True)
			# 执行sql语句
			cur.execute(sql)
			# 获取结果
			result = cur.fetchall()
			# 关闭
			self.close_conn(conn, cur)
			# 返回查询结果
			return result
			
		except Exception as e:
			# 如果发生错误则回滚
			conn.rollback()
			# 关闭
			self.close_conn(conn, cur)
			# 日志记录
			msg = db_name+'  '+sql + '  '+ str(e)
			# CustomLogger().log_writter(msg)
			
			
	def operate(self, action, db_name, sql):
		# action：必选，只能填 insert，delete，update
		# db_name：创建哪个模块的数据库连接池
		# sql: 需要删除数据库的sql query
		# 增，删，改
		
		# 检查action是否符合规范
		if action in ('insert','delete','update'):
		
			# 创建链接和操作游标
			conn, cur = self.create_conn(db_name)
			try:
				# 如果数据库连接失败，则重连
				conn.ping(reconnect=True)
				# 执行sql语句
				cur.execute(sql)
				# 提交
				conn.commit()
			except Exception as e:
				# 如果发生错误则回滚
				conn.rollback()

				# 忽略因为收集的IP与库中现存的IP重复出现的日志信息
				if db_name == 'parser_component' and e.args[0] == 1062:
					pass
				else:
					# 日志记录
					msg = db_name+'  '+sql + '  '+ str(e)
					# custom_logger.CustomLogger().log_writter(msg)

			finally:
				# 关闭
				self.close_conn(conn, cur)
		else:
			# print("Wrong action,please reinput one")
			# 检查action不符合规范，只能填 insert，delete，update
			# 日志记录
			msg = "Wrong action,please reinput one, choose from (insert，delete，update)"
			# custom_logger.CustomLogger().log_writter(msg)


if __name__ == "__main__":
	go = DBOperator()
	# conn, cursor = go.create_conn('parser_component')
	#print(conn)
	#print(cursor)
	#sql = """INSERT INTO `parser_component`.`IP_availability`(`ip_address`, `is_anonymous`, `is_available`, `type`) VALUES ('103.39.214.69:8118', 1, 1, 'HTTP');"""
	#go.operate('insert','parser_component',sql)
