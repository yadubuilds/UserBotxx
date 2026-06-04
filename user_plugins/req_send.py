import time, asyncio, datetime, asyncio, logging, csv

from config import Config 
from pyrogram import Client, filters, enums, raw
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from helper.utils import get_time

# -------- Tunables --------
CONCURRENCY = 10
BATCH_SIZE = 25
MAX_RETRIES = 5
MAX_FLOODWAIT = 600
PAUSE = 0.5
# --------------------------


def failed_csv(chat_id: int):
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    return f"failed_join_requests_{chat_id}_{ts}.csv"


@Client.on_message(filters.command("rs") & filters.user('self') & filters.chat('me') & filters.reply)
async def rs_handler(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\nReply to message and type:\n/rs -100xxxxxxxxxx",
            quote=True
        )

    chat_id = int(message.command[1])
    content = message.reply_to_message
    start = time.time()

    done = success = failed = skipped = 0
    failed_ids = []

    sts = await message.reply_text("Broadcast started", quote=True)

    sem = asyncio.BoundedSemaphore(CONCURRENCY)
    batch = []

    async def send(uid):
        async with sem:
            ok = await send_with_retry(client, content, uid)
            return uid if not ok else None


    async for req in client.get_chat_join_requests(chat_id):

        user = getattr(req, "user", None)

        if not user or user.is_bot:
            skipped += 1
            done += 1
            continue

        batch.append(asyncio.create_task(send(user.id)))
        done += 1

        if len(batch) >= BATCH_SIZE:

            results = await asyncio.gather(*batch)
            batch.clear()

            for r in results:
                if r is None:
                    success += 1
                else:
                    failed += 1
                    failed_ids.append(r)

            await sts.edit(
                f"Sending...\n\n"
                f"Done: {done}\n"
                f"Success: {success}\n"
                f"Failed: {failed}\n"
                f"Skipped: {skipped}"
            )

            await asyncio.sleep(PAUSE)


    if batch:
        results = await asyncio.gather(*batch)

        for r in results:
            if r is None:
                success += 1
            else:
                failed += 1
                failed_ids.append(r)


    if failed_ids:
        with open(failed_csv(chat_id), "w", newline="") as f:
            csv.writer(f).writerows([("user_id",)] + [(i,) for i in failed_ids])


    await sts.edit(
        f"Completed in {get_time(int(time.time()-start))}\n\n"
        f"Done: {done}\nSuccess: {success}\nFailed: {failed}\nSkipped: {skipped}"
    )


async def send_with_retry(client, msg, uid: int) -> bool:

    delay = 1

    for _ in range(MAX_RETRIES):

        try:
            await msg.copy(uid)
            return True

        except FloodWait as e:
            if e.value > MAX_FLOODWAIT:
                return False
            await asyncio.sleep(e.value + 1)

        except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid):
            return False

        except Exception:

            try:
                if msg.text:
                    await client.send_message(uid, msg.text)
                    return True
            except FloodWait as e:
                if e.value > MAX_FLOODWAIT:
                    return False
                await asyncio.sleep(e.value + 1)

            await asyncio.sleep(delay)
            delay = min(delay * 2, 30)

    return False