from sql_commands import filter_title_author_review_date_read



def get_main_page_data(conn) -> dict:     
    statement = filter_title_author_review_date_read(conn)
    lst = ["Title", "Author", "Review", "Date read"]
    main_dict = {}
    counter = 0
    for row in statement:
        row_dict = {}
        for index, data in enumerate(row):
            row_dict[lst[index]] = data
        counter+=1
        main_dict[counter] = row_dict
    conn.close()
    return main_dict