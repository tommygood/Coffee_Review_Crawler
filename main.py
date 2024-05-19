import requests

# site url
site_url = "https://www.coffeereview.com/top-30-coffees/"
# the columns are needed on the site
necessary_object = ["Est. Price:", "Aroma", "Acidity", "Body", "Flavor", "Aftertaste"]

# get the url of each coffee site
def getEachCoffeeUrl() :
    headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}
    result = requests.get(site_url, headers=headers)
    text = result.text
    match_text = '<a href="'
    index = 0
    temp_href = ""
    start_record_href = False
    all_href = []
    for i in range(len(text)) :
        if start_record_href :
            if text[i] == '"' :
                # stop record href
                start_record_href = False
                # put this href into list
                all_href.append(temp_href)
                # clear the temp href
                temp_href = ""
            else : 
                temp_href += text[i]
        if text[i] == match_text[index] :
            index += 1
            if index == len(match_text) :
                # start record content of href in <a> tag
                start_record_href = True
                index = 0
    # get the href that are the info about each coffee
    all_real_href = []
    for i in range(len(all_href)) :
        if "/review/" in all_href[i] and len(all_href[i]) > 36 :
            all_real_href.append(all_href[i])
    # filter the same href
    all_real_href = list(set(all_real_href))
    return all_real_href

# get info of each type of coffee from different site
def getEachCoffeeInfo(all_url) :
    headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}
    all_coffee_info = {}
    for i in range(len(all_url)) :
        print("crawling the", all_url[i])
        result = requests.get(all_url[i], headers=headers)
        text = result.text
        name = all_url[i][36:len(all_url[i])-1]
        temp = {}
        for j in range(len(necessary_object)) :
            obj = necessary_object[j]
            if obj in text :
                start_index = text.index(obj)
                count_close_td = 0
                index = 0
                td_text = '<td>'
                close_td_text = "</td>"
                clost_td_index = 0
                value = ""
                count_td = 0
                while count_close_td < 2 and start_index < len(text) :
                    if count_td > 1 :
                        value += text[start_index]
                    if text[start_index] == td_text[index] :
                        # if match a index of <td>
                        index += 1
                        if (index == len(td_text)) :
                            index = 0
                            count_td += 1
                    if text[start_index] == close_td_text[clost_td_index] :
                        # if match a index of <td>
                        clost_td_index += 1
                        if (clost_td_index == len(close_td_text)) :
                            count_close_td += 1
                            clost_td_index = 0
                    start_index += 1
                # specify deal with the Body column
                if obj == "Body" :
                    n_value = ""
                    for k in range(len(value)) :
                        if (value[k].isdigit()) :
                            n_value += value[k]
                    value = n_value + "     "
                temp[obj] = value[:len(value)-5]
            else :
                print("column %s not found int the text of url %s" % (obj, all_url[i]))
        all_coffee_info[name] = temp
    return all_coffee_info

# entry point
def main() :
    # get the url of each coffee site
    all_url = getEachCoffeeUrl()
    # get info of each type of coffee from different site
    all_coffee_info = getEachCoffeeInfo(all_url)
    print(all_coffee_info)

main()