def find_index(list, id):
    indexComponent = -1
    for _, item in enumerate(list):
        if (str(item["id"]) == str(id)):
            indexComponent = _
            break
    return indexComponent