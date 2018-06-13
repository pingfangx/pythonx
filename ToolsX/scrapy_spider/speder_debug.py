import asyncio

import asyncpg
from scrapy import cmdline
from scrapy_spider.ignore.postgreconfig import postgre_configs
from scrapy_spider.items import AwemeItem
from scrapy_spider.pipelines import PostgreSQLPipeline


def connect_db():
    conn = asyncpg.connect(**postgre_configs)
    conn.close()


def run_spider_to_json():
    spider = "douyin"
    args = "-o items.json"
    cmd = "scrapy crawl %s %s" % (spider, args)
    cmdline.execute(cmd.split())


def run_spider():
    spider = "douyin"
    args = ""
    cmd = "scrapy crawl %s %s" % (spider, args)
    cmdline.execute(cmd.split())


def generate_create_table_sql():
    """
    生成
    :return:
    """
    item = AwemeItem()
    field_str = ''
    field_str += '"id" serial PRIMARY KEY NOT NULL,\n'
    for key in item.fields.keys():
        field_str += f'"{key}" text NOT NULL,\n'
    # 去掉逗号
    field_str = field_str.rstrip(',\n')
    field_str += '\n'

    table_name = 'douyin'
    sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n{field_str});"

    table_name = "{self.table_name}"
    print_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n{field_str});"
    print_sql = "f'''\n%s\n'''" % print_sql
    print(print_sql)

    return sql


def create_table():
    asyncio.get_event_loop().run_until_complete(execute(generate_create_table_sql()))


async def execute(sql):
    print("执行", sql)
    conn = await asyncpg.connect(**postgre_configs)
    await conn.execute(sql)
    await conn.close()


def insert_item():
    item = AwemeItem(desc_="test", create_time=1)
    pipe = PostgreSQLPipeline()
    pipe.open_spider('')
    pipe.process_item(item, None)


if __name__ == '__main__':
    run_spider()
    # connect_db()
    # generate_create_table_sql()
    # create_table()
    # insert_item()
    pass
