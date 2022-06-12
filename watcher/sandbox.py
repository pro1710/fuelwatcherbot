import helpers


def main():
   
    user_location = {
        'latitude':  50.370697,
        'longitude': 30.464447 
    }


    df = helpers.read_pickle('./data/wog/last.pkl')

    print(df.info())


if __name__ == '__main__':
    main()



