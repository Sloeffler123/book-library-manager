from sql_files.sql_commands import filter_title_author_review_date_read


def get_main_page_data(conn) -> dict:
    statement = filter_title_author_review_date_read(conn)
    lst = ["title", "author", "review", "date_read"]
    main_dict = {}
    for counter, row in enumerate(statement):
        row_dict = {}
        for index, data in enumerate(row):
            row_dict[lst[index]] = data
        main_dict[str(counter)] = row_dict
    conn.close()
    return main_dict
