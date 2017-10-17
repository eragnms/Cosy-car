Class Heater():
    zwave_id = 
    start_time =
    stop_time =
  
Class TestEngine():
    while test_case_should run:
        if should cosy_car_run:
            cosycar -check  
            heater_statuses = check_heater_statuses()
            for heater in self.heaters:
                if heater.should_run(time) != heater_statuses[heater.zwave_id]:
                    raise failure
        

Class TestWhatever():
    def __init__():
        block_heater = Heater(x,y,z)
        comp_heater = Heater(x,y,z)
        self.heaters = [block_heater, comp_heater]
        run_time = 
    def run():
        cosycar force start in 30 min
        test_engine = TestEngine(self.run_time)
              

Class TestSomethingElse()

def init_test_cases()
    test_1 = TestWhatever()
    test_2 = TestSomethingElse()
    test_cases[test_1, test_2]
    return test_cases

main()
    test_cases = init_test_cases()
    for test_case in test_cases:
        setup()
        try:
            test_case.run()
        except:
            raise error or wait until all tests have run
        teardown()
