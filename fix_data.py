import os

count = 0
att_deleted = 0
dirs_deleted = 0
agencies = []
agencies_complete = 0


def is_json(filename):
    if str(filename).endswith('.json'):
        return True
    return False


def delete_empty_dir(path):
    global dirs_deleted
    if (len(os.listdir(path)) == 0): # if directory is empty
        os.rmdir(path) # delete directory at that path
        dirs_deleted += 1


def delete_attachment(path):
    global att_deleted
    os.remove(path)
    att_deleted += 1


def get_agencies(dir):
    global agencies 
    with os.scandir(dir) as it:
        for agency in it:
            agencies.append(agency.name)


def check_and_remove_attachments(dir):
    global count, agencies_complete
    print('\rDocs found: {}, Agencies completed: {}, Empty Dir Deleted: {}, Attachments Deleted: {}'.format(count, agencies_complete - 1, dirs_deleted, att_deleted), end='')

    with os.scandir(dir) as it:
        for entry in it: # for each object in curr dir
            count += 1

            if entry.name in agencies:
                agencies_complete += 1
                
            if not os.path.isdir(entry): # if not a directory
                if not is_json(entry.name): # if not .json file
                    delete_attachment(entry)
            else:  
                check_and_remove_attachments(entry)
                delete_empty_dir(entry) # this need to be last so if it becomes empty after moving files, still delete
            

def main():
    data_dir = os.path.expanduser("~/data/data")
    get_agencies(data_dir)
    check_and_remove_attachments(data_dir)
    print("\nComplete")


if __name__ == "__main__":

    main()


# 
# check if a file is not .json, move to data/attachments(new dir)
# check if dir is empty. If it is, delete it.
# 


