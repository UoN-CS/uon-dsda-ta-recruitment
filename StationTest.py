from Station import Station

def main():
    label = 'Stanmore, Wolverton Road'
    station = Station(label)

    print(station)

    df = station.getWaterLeveldf()

    print(df)

if __name__ == '__main__':
    main()