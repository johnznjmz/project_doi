BOT_NAME = 'scrapyspider'

SPIDER_MODULES = ['project_doi.scrapyspider.spiders']
NEWSPIDER_MODULE = 'project_doi.scrapyspider.spiders'


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 " \
             "Safari/537.36 "
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

#CONCURRENT_REQUESTS = 32


#DOWNLOAD_DELAY = 3
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

#COOKIES_ENABLED = False

#TELNETCONSOLE_ENABLED = False

#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

#SPIDER_MIDDLEWARES = {
#    'scrapyspider.middlewares.MyprojectspSpiderMiddleware': 543,
#}

#DOWNLOADER_MIDDLEWARES = {
#    'scrapyspider.middlewares.MyprojectspDownloaderMiddleware': 543,
#}

#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

ITEM_PIPELINES = {
    'project_doi.scrapyspider.pipelines.DefaultValuesPipeline': 300,
    # 'scrapyspider.pipelines.WileyPipeline': 800,
}

#AUTOTHROTTLE_ENABLED = True
#AUTOTHROTTLE_START_DELAY = 5
#AUTOTHROTTLE_MAX_DELAY = 60

#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
#AUTOTHROTTLE_DEBUG = False

#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
