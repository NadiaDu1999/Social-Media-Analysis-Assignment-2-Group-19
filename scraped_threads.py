#This code will lead us to get the threads post and replies from the given URL
# have to change URL each time

import json
from typing import Dict

import jmespath
from parsel import Selector
from nested_lookup import nested_lookup
from playwright.sync_api import sync_playwright


def parse_thread(data: Dict) -> Dict:
    """Parse Twitter tweet JSON dataset for the most important fields"""
    result = jmespath.search(
        """{
        text: post.caption.text,
        published_on: post.taken_at,
        id: post.id,
        pk: post.pk,
        code: post.code,
        username: post.user.username,
        reply_count: view_replies_cta_string,
        like_count: post.like_count,
        videos: post.video_versions[].url
    }""",
        data,
    )
    
    if result.get("reply_count") and not isinstance(result["reply_count"], int):
        try:
            result["reply_count"] = int(result["reply_count"].split(" ")[0])
        except Exception:
            result["reply_count"] = None
    result["url"] = f"https://www.threads.net/@{result['joelleqnunez']}/post/{result['DHuE901y7V2?hl=en']}"
    return result

    # result["videos"] = list(set(result["videos"] or []))
    # if result["reply_count"] and type(result["reply_count"]) != int:
    #     result["reply_count"] = int(result["reply_count"].split(" ")[0])
    # result[
    #     "url"
    # ] = f"https://www.threads.com/@{result['username']}/post/{result['code']}"
    # return result


import json
from parsel import Selector
from nested_lookup import nested_lookup
from playwright.sync_api import sync_playwright

def scrape_thread(url: str) -> dict:
    """Scrape Threads post and replies from a given URL"""
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        page.goto(url)
        page.wait_for_selector("[data-pressable-container=true]")

        selector = Selector(text=page.content())
        hidden_datasets = selector.css('script[type="application/json"][data-sjs]::text').getall()

        for hidden_dataset in hidden_datasets:
            if '"ScheduledServerJS"' not in hidden_dataset or "thread_items" not in hidden_dataset:
                continue

            data = json.loads(hidden_dataset)
            thread_items = nested_lookup("thread_items", data)

            if not thread_items:
                raise ValueError("Could not find thread data in page")

            # Just return the raw data for now — customize parsing as needed
            return thread_items

        raise ValueError("Thread data not found in any script tag")

if __name__ == "__main__":
    url = "https://www.threads.com/@joelleqnunez/post/DHuE901y7V2?hl=en"
    result = scrape_thread(url)
    print(json.dumps(result, indent=2))




# import json
# import jmespath
# from typing import Dict
# from parsel import Selector
# from nested_lookup import nested_lookup
# from playwright.sync_api import sync_playwright


# def parse_thread(data: Dict) -> Dict:
#     """Extract important thread fields using JMESPath"""
#     result = jmespath.search(
#         """{
#             text: post.caption.text,
#             published_on: post.taken_at,
#             id: post.id,
#             pk: post.pk,
#             code: post.code,
#             username: post.user.username,
#             user_pic: post.user.profile_pic_url,
#             user_verified: post.user.is_verified,
#             user_pk: post.user.pk,
#             user_id: post.user.id,
#             has_audio: post.has_audio,
#             reply_text: I want to get replies of that threads from here
#             reply_count: view_replies_cta_string,
#             like_count: post.like_count,
#             images: post.carousel_media[].image_versions2.candidates[1].url,
#             image_count: post.carousel_media_count,
#             videos: post.video_versions[].url
#         }""",
#         data,
#     )
#     result["videos"] = list(set(result["videos"] or []))
#     if result.get("reply_count") and not isinstance(result["reply_count"], int):
#         result["reply_count"] = int(result["reply_count"].split(" ")[0])
#     result["url"] = f"https://www.threads.net/@{result['@faerieaus']}/post/{result['DHQR_KJSgyR']}"
#     return result


# def scrape_thread(url: str) -> dict:
#     """Scrape Threads post JSON from page source"""
#     with sync_playwright() as pw:
#         browser = pw.chromium.launch()
#         context = browser.new_context()
#         page = context.new_page()
#         page.goto(url)
#         page.wait_for_selector("[data-pressable-container=true]")

#         selector = Selector(text=page.content())
#         hidden_datasets = selector.css('script[type="application/json"][data-sjs]::text').getall()

#         for hidden_dataset in hidden_datasets:
#             if '"ScheduledServerJS"' not in hidden_dataset or "thread_items" not in hidden_dataset:
#                 continue

#             data = json.loads(hidden_dataset)
#             thread_items = nested_lookup("thread_items", data)
#             if not thread_items:
#                 continue

#             # take the first post for simplicity
#             return parse_thread(thread_items[0][0])

#         raise ValueError("Could not find thread data in page")

# if __name__ == "__main__":
#     url = "https://www.threads.net/@faerieaus/post/DHQR_KJSgyR"
#     result = scrape_thread(url)
#     print(json.dumps(result, indent=2))
