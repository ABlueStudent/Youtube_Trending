from bs4 import BeautifulSoup
import requests
import csv
import time


class Youtube:
    cache = requests.get("https://www.youtube.com/feed/trending").text
    soup = BeautifulSoup(cache, "html.parser").findAll("div", "feed-item-dismissable")

    
    def trending(self):
        return self.soup[0].find("div", "expanded-shelf").find("ul", "expanded-shelf-content-list has-multiple-items").findAll("li", "expanded-shelf-content-item-wrapper")


    def recent_trending(self):
        return self.soup[1].find("div", "expanded-shelf").find("ul", "expanded-shelf-content-list has-multiple-items").findAll("li", "expanded-shelf-content-item-wrapper")


    def sorted_trending(self):
        sorted_trending = list(
            map(
                lambda data: {
                    "title": data.find("a", "yt-uix-tile-link").get("title"),
                    "length": data.find("span").text.replace("\n", ""),
                    "upload_time": data.find("ul", "yt-lockup-meta-info").findAll("li")[0].text.replace("\n", ""),
                    "viewers": data.find("ul", "yt-lockup-meta-info").findAll("li")[1].text.replace("\n", "").split("：")[1],
                    "owner": data.find("div", "yt-lockup-byline").text.replace("\n", "").replace("\xa0", ""),
                    "url": "https://www.youtube.com" + data.find("a", "yt-uix-tile-link").get("href")
                },
                self.trending()
            )
        )
        return sorted_trending


    def sorted_recent_trending(self):
        sorted_recent_trending = list(
            map(
                lambda data: {
                    "title": data.find("a", "yt-uix-tile-link").get("title"),
                    "length": data.find("span").text.replace("\n", ""),
                    "upload_time": data.find("ul", "yt-lockup-meta-info").findAll("li")[0].text.replace("\n", ""),
                    "viewers": data.find("ul", "yt-lockup-meta-info").findAll("li")[1].text.replace("\n", "").split("：")[1],
                    "owner": data.find("div", "yt-lockup-byline").text.replace("\n", "").replace("\xa0", ""),
                    "url": "https://www.youtube.com" + data.find("a", "yt-uix-tile-link").get("href")
                },
                self.recent_trending()
            )
        )
        return sorted_recent_trending


def Main():
    YT_Trending = Youtube()
    YT_Sorted_Trending = YT_Trending.sorted_trending()
    YT_Sorted_Recent_Trending = YT_Trending.sorted_recent_trending()
    filename = str(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))

    with open(filename + ".csv", "w", newline="", encoding="utf-8-sig") as csvfile:
        fieldnames = ["title", "length", "upload_time", "viewers", "owner", "url"]
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writerow({"title": "Trending"})
        writer.writerow({"title": "標題", "length": "影片長度", "upload_time": "上傳時間", "viewers": "觀看次數", "owner": "頻道", "url": "連結"})
        for data in YT_Sorted_Trending:
            writer.writerow(data)
        writer.writerow({})
        writer.writerow({"title": "Recent Trending"})
        writer.writerow({"title": "標題", "length": "影片長度", "upload_time": "上傳時間", "viewers": "觀看次數", "owner": "頻道", "url": "連結"})
        for data in YT_Sorted_Recent_Trending:
            writer.writerow(data)


if __name__ == "__main__":
    Main()
