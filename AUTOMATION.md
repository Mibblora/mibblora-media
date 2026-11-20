# Mibblora Instagram automation – rules for every scheduled run

Channel: Instagram @mibblora (account id 17841414745417204 on the Windsor.ai connector "instagram").
Audience: parents, grandparents, teachers of kids 3-6 in the US (books sold on amazon.com).
Everything on the channel is in ENGLISH. Talk to the owner in German.

## Each run
1. Today's date in America/New_York. Find today's entry in plan.json (christmas_phase by date, else rotation by weekday). No entry -> stop quietly, send nothing.
2. Read log/posts.json to avoid repeating pages, hooks or captions of the last 30 posts.
3. Build the content from books/<book>/ (see books/README.md). Use only live books. Never show German text (christmas-stars interior is German: use only its pictures, crop away text).
4. Reel: 1080x1920, 12-18 s, hook card in first 2 s, max 6 words per text card, real cover as end card + "Link in bio". Embed self-made music that fits the book (see tools/music_example.py; Christmas = music box/bells, dino = playful, unicorn = dreamy). Encode: H.264 main, level 4.0, 30 fps, -bf 0, -g 30, yuv420p, AAC 128k 48 kHz stereo, +faststart.
   Carousel / image: JPEG 1080x1350, max 8 MB, slide 1 = hook <= 6 words, last slide = "Link in bio".
   Style: navy (14,27,56) background, gold (236,196,104) Cardo Bold headlines, cream Montserrat body, snow dots for Christmas. See tools/make_reel_example.py.
5. Caption: English, first line is the hook (works within ~125 chars), 1-3 short lines, one CTA ("Link in bio" or "Save this"), max 5 hashtags, no em dashes, no "comment KEYWORD" (nobody answers DMs), never invent reviews/numbers.
6. Commit media to the repo (reels/ or posts/<date>/), push, wait 120 s for GitHub Pages.
   Public URL: https://mibblora.github.io/mibblora-media/<path>
7. Publish via METRICOOL (connector "Metricool_Social_Media_Management", brand blogId "8246366", brand timezone Europe/Berlin). Use createScheduledPost with media = public GitHub Pages URL(s), providers [{"network":"instagram"}], autoPublish true, and schedule it for 20:00 America/New_York today (publicationDate dateTime in that zone, timezone "America/New_York"; the date param as ISO 8601 with the matching offset). instagramData.type: "REEL" (video, showReelOnFeed true, videoCoverMilliseconds ~1200), "POST" (single image or carousel = several image URLs in media), "STORY" (no text). Set isAiGenerated only if the visuals are AI-made (the owner decides; default false).
   Reels work via Metricool (first reel published 2026-11-20). Windsor's create_video_post is broken (refs 51667833, 51683601, 51690778); use Windsor only as a fallback for images if Metricool fails, and for reading analytics.
   After scheduling, check with getScheduledPosts (around the publish time if the run is still active) or trust the "PENDING" status; record the plannerUrl.
8. Stories (image only, every posting day, after the feed post): publish 1-2 image stories via Windsor create_story (image_url). JPEG 1080x1920, key content inside y 250-1650 (top/bottom are covered by Instagram UI). Ideas: an inside page or story picture with a short line ("Meet Fina", "Peek inside"), and a teaser for today's post ("New post" + post visual). Same navy/gold style. No stickers or links are possible via the API, so do not write "tap here"; use "New post on our profile" or "Link in bio". Video stories are allowed via Metricool. Render book pages at 300 dpi so story images stay sharp. Save under stories/<date>/ and log them.
9. Append to log/posts.json: date, format, book, idea, hook, pages used, caption, media id or failure, reel_manual (true/false). Commit + push.
10. Tell the owner in German, short: what was posted (with permalink if known), and if a reel needs manual upload, send the file and the caption ready to copy.

## Never
- Post anything about books not live on amazon.com (not christmas-dreams, not Dino-Spass/German books).
- Show children's faces, fake reviews, prices or delivery promises you did not verify.
- Follow, like, comment or DM.
