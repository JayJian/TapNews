import cnn_news_scraper as scraper

EXPECTED_STRING = "Pope Francis has drawn a rebuke from the American Jewish Committee after he likened European refugee centers to "
CNN_NEWS_URL = "http://www.cnn.com/2017/04/23/europe/pope-likens-refugee-centers-to-concentration-camps/index.html"

def test_basic():
    news = scraper.extract_news(CNN_NEWS_URL)

    assert EXPECTED_STRING in news
    print news
    print 'test_basic passed!'

if __name__ ==  "__main__":
    test_basic()
