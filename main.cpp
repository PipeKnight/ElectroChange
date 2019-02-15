#include <iostream>
#include <fstream>
#include <iomanip>
#include <math.h>
#include <vector>
#include <algorithm>

using namespace std;

const int N = 4;
const int M = 1000 * 1000;

// all "Base" values are actual for 2018 year
const long double InflationOfPrice = 1.05;
const long long   BasePriceOfBus = 12820 * 1000;
const long double BasePriceOfElectr = 5.38; // can check from net
const long double BasePriceOfFuel = 44.33; // can check from net
const long long   BaseSalary = 56000;
const long long   BasePriceOfContactNetwork = 8 * 1000 * 1000; // per kilometer
const long long   BasePriceOfElectrobus = 33 * 1000 * 1000; // электробусы с быстрой зарядкой
const long long   BasePriceOfTrolleybus1 = 15 * 1000 * 1000; // обычные троллейбусы
const long long   BasePriceOfTrolleybus2 = 20 * 1000 * 1000; // с автономным ходом
const long long   BasePriceOfElectrobus2 = 33 * 1000 * 1000; // с ночной зарядкой
const long long   PriceOfChargingStation = 13 * 1000 * 1000;
const int BaseServiceOfContactNetwork = 5000 * 12; // per year
const int BaseServiceOfChargingStation = 44600 * 12; // per year


const long double ElectrConsumption = 2.32; // per kilometer
const int LifeOfBus = 5; // 5 or 6 years
const int LifeOfElectrobus = 13; // 15 years, but battery lives less
const int LifeOfTrolleybus1 = 11; // 11 or 12 years
const int LifeOfTrolleybus2 = 11; // 11 or 12 years
const int LifeOfElectrobus2 = 12; // "we do not know" years


pair<long long, pair<vector<long long>, vector<long long>>> Calc(const string &Route, int Date) {
    // We need "Date" if we want to calculate other years (for far perspective, maybe)
    ifstream in("data/calcdata/" + Route + ".txt");
    int Bus = 0;
    long double Length = 0, Cnt = 0, FuelConsumption = 0, Electr = 0;
    long long ServiceOfBusPerYear = 0;
    vector<long long> CostOfPurchases(N, 0), CostOfSerPerYear(N, 0), DriverSalary(N, 0), NewBus(N, 0);
    long double Inflation = pow(InflationOfPrice, Date - 2018);
    long double PriceOfBus = BasePriceOfBus * Inflation;
    long double PriceOfElectrobus = BasePriceOfElectrobus * Inflation;
    long double PriceOfTrolleybus1 = BasePriceOfTrolleybus1 * Inflation;
    long double PriceOfTrolleybus2 = BasePriceOfTrolleybus2 * Inflation;
    long double PriceOfElectrobus2 = BasePriceOfElectrobus2 * Inflation;
    long double PriceOfContactNetwork = BasePriceOfContactNetwork * Inflation;
    long double PriceOfElectr = BasePriceOfElectr * Inflation;
    long double PriceOfFuel = BasePriceOfFuel * Inflation;
    long double Salary = BaseSalary * Inflation;
    long double ServiceOfContactNetwork = BaseServiceOfContactNetwork * Inflation;
    long double ServiceOfChargingStation = BaseServiceOfChargingStation * Inflation;

    in >> Length; // Протяженность маршрута (туда и обратно) в километрах
    in >> Cnt; // Сколько раз за год автобус в среднем проходит маршрут
    in >> Bus; // Количество автобусов на маршруте
    in >> Electr; // Процерт маршрута покрыт контактной сетью
    in >> FuelConsumption; // Расход топлива на 100 км

    FuelConsumption /= 100;
    NewBus[0] = Bus * 3 / 2;
    NewBus[1] = Bus;
    NewBus[2] = Bus;
    NewBus[3] = Bus;
    DriverSalary[0] += Salary * NewBus[0] * 2;
    DriverSalary[1] += Salary * NewBus[1] * 2;
    DriverSalary[2] += Salary * NewBus[2] * 2;
    DriverSalary[3] += Salary * NewBus[3] * 2;
    CostOfPurchases[0] += (NewBus[0] * PriceOfElectrobus)  + (NewBus[0] * PriceOfChargingStation * 2 / 3);
    CostOfPurchases[1] += (NewBus[1] * PriceOfTrolleybus1) + (Length * PriceOfContactNetwork * (100 - Electr) / 100);
    CostOfPurchases[2] += (NewBus[2] * PriceOfTrolleybus2) + (Length * PriceOfContactNetwork * max(0.0 * Electr, 50 - Electr) / 100);
    CostOfPurchases[3] += (NewBus[3] * PriceOfElectrobus2) + (NewBus[3] * PriceOfChargingStation / 10);
    CostOfSerPerYear[0] += (PriceOfElectrobus * NewBus[0]  / LifeOfElectrobus)  + ((NewBus[0]  * 2 / 3) * ServiceOfChargingStation) + (NewBus[0] * Length * (Cnt / 2) * (FuelConsumption / 2) * PriceOfFuel);
    CostOfSerPerYear[1] += (PriceOfTrolleybus1 * NewBus[1] / LifeOfTrolleybus1) + (Length * ServiceOfContactNetwork)                + (NewBus[1] * Length * Cnt * ElectrConsumption * PriceOfElectr);
    CostOfSerPerYear[2] += (PriceOfTrolleybus2 * NewBus[2] / LifeOfTrolleybus2) + ((Length / 2) * ServiceOfContactNetwork)          + (NewBus[2] * Length * Cnt * ElectrConsumption * PriceOfElectr);
    CostOfSerPerYear[3] += (PriceOfElectrobus2 * NewBus[3] / LifeOfElectrobus2) + ((NewBus[3] / 10) * ServiceOfChargingStation)     + (NewBus[3] * Length * (Cnt / 2) * (FuelConsumption / 2) * PriceOfFuel);
    ServiceOfBusPerYear += (PriceOfBus * Bus / LifeOfBus) + (Bus * Length * Cnt * FuelConsumption * PriceOfFuel);
    CostOfSerPerYear[0] += DriverSalary[0] * 12;
    CostOfSerPerYear[1] += DriverSalary[1] * 12;
    CostOfSerPerYear[2] += DriverSalary[2] * 12;
    CostOfSerPerYear[3] += DriverSalary[3] * 12;
    ServiceOfBusPerYear += DriverSalary[1] * 12;
    return make_pair(ServiceOfBusPerYear, make_pair(CostOfPurchases, CostOfSerPerYear));
}


void Print(const pair<long long, pair<vector<long long>, vector<long long>>> &ans) {
    auto ServiceOfBusPerYear = ans.first;
    auto CostOfPurchases = ans.second.first;
    auto CostOfSerPerYear = ans.second.second;
    cout << setprecision(3) << fixed;
    cout << "Сколько нужно начальных инвестиций (в млн рублей) для замены дизельных автобусов на:\n";
    cout << "\t -- электробусы: " << CostOfPurchases[0] * 1.0 / M << endl;
    cout << "\t -- троллейбусы: " << CostOfPurchases[1] * 1.0 / M << endl;
    cout << "\t -- троллейбусы с автономным ходом: " << CostOfPurchases[2] * 1.0 / M << endl;
    //cout << "\t -- электробусы с ночной зарядкой: " << CostOfPurchases[3] * 1.0 / M << endl;
    cout << endl;
    cout << "Во сколько будет обходиться обслуживание в год в млн рублей (учитывая амортизационную стоимость):\n";
    cout << "\t -- автобусы: " << ServiceOfBusPerYear * 1.0 / M << endl;
    cout << "\t -- электробусы: " << CostOfSerPerYear[0] * 1.0 / M << endl;
    cout << "\t -- троллейбусы: " << CostOfSerPerYear[1] * 1.0 / M << endl;
    cout << "\t -- троллейбусы с автономным ходом: " << CostOfSerPerYear[2] * 1.0 / M << endl;
    //cout << "\t -- электробусы с ночной зарядкой: " << CostOfSerPerYear[3] * 1.0 / M << endl;
    cout << endl;
}


int main() {
    setlocale(LC_ALL, "Russian");

    ifstream R("data/works.txt");
    vector<string> CorrectRoutes;
    string t;
    while (R >> t) {
        CorrectRoutes.push_back(t);
    }

    string Route;

    cout << "Введите:\n\tA) номер маршрута, если хотите посчитать для конкретного маршрута\n\tБ) -1, если хотите посчитать для всех маршрутов сразу\n\tВ) -2, если хотите завершить работу\n";
    cin >> Route;
    while (Route != "-2") {
        if (Route == "-1") {
            auto ans = Calc(CorrectRoutes[0], 2018);
            for (auto i = 1; i < CorrectRoutes.size(); ++i) {
                auto t = Calc(CorrectRoutes[i], 2018);
                ans.first += t.first;
                for (auto i = 0; i < N; ++i) {
                    ans.second.first[i] += t.second.first[i];
                    ans.second.second[i] += t.second.second[i];
                }
            }
            Print(ans);
        } else {
            if (find(CorrectRoutes.begin(), CorrectRoutes.end(), Route) == CorrectRoutes.end()) {
                cout << "Введён неправильный номер" << endl;
            } else {
                auto ans = Calc(Route, 2018);
                Print(ans);
            }
        }
        cin >> Route;
    }
}
