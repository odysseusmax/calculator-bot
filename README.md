# Calculator Bot

Example of Python Serverless Telegram bot to be used with <https://vercel.com>

## Steps

### Add env variable to vercel.com

Add your telegram bot token as `BOT_TOKEN` variable

### Register webhook

``` bash
curl "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=https://your-project-name.vercel.app/api/webhook"
```
