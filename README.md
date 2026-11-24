# Telegram Image Bot — Vercel

A webhook-based Telegram bot. It reads image/page URLs from the `IMAGE_LINKS` list in `api/webhook.py`, selects one working image, and sends one photo when `/image` is used in a group. Only `BOT_TOKEN` is needed as a Vercel environment variable.

## 1. Put the files on GitHub

Upload this folder's contents to a GitHub repository. Open `api/webhook.py` and edit the `IMAGE_LINKS` list near the top. Add one public image or webpage URL per item, keeping each URL in quotes. Direct image URLs and public webpages with Open Graph/Twitter image metadata or ordinary `<img>` tags are supported.

## 2. Deploy on Vercel

1. Import the GitHub repository into Vercel.
2. Add only one Environment Variable under Project Settings → Environment Variables:
   - `BOT_TOKEN`: token from `@BotFather`
3. Deploy. Your function endpoint will be `https://YOUR-PROJECT.vercel.app/api/webhook`.

## 3. Register the Telegram webhook

Open this URL in a browser after replacing the values:

`https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook?url=https://YOUR-PROJECT.vercel.app/api/webhook`

Telegram should return `{"ok":true,...}`.

## 4. Add the bot to a group

Add the bot to your group and allow it to send photos. In BotFather, use `/setprivacy` and disable privacy if you need the bot to react to `/image` when it is not mentioned; command messages normally work with privacy enabled. Test with `/image`.

## Notes

- This is a serverless webhook, not a long-running polling bot.
- The bot sends one image per `/image` command. It randomizes the URL order and sends the first working image it finds.
- Some websites block automated access or load images with JavaScript; those pages may not work. Use direct, publicly accessible image URLs when possible.
- The image must be publicly accessible to Telegram's servers. The bot does not bypass logins, paywalls, or access restrictions.
- Do not commit your bot token to GitHub. Store it only in Vercel environment variables.
- Vercel's serverless functions have execution limits. Large URL lists or slow websites may time out; keep the list reasonably sized.
