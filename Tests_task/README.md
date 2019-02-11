Unit tests for module person

Failures:
1. test_person_get_age
    >       now = datetime.datetime.now()
    > NameError: name 'datetime' is not defined
    
        def get_age(self):
        now = datetime.datetime.now()
        return self.yob - now.year

2. test_person_get_age
   >       assert person.get_age() == 220
   > Error: assert -220 == 220
   
        def get_age(self):
        now = datetime.datetime.now()
        return self.yob - now.year

3. test_person_set_name
    >       assert person.name == 'Sasha'
    > AssertionError: assert 'Alexander' == 'Sasha'
    
        def set_name(self, name):
        self.name = self.name

4. test_set_address
    >       assert person.address == 'Spb'
    > AssertionError: assert 'Moscow' == 'Spb'
    
        def set_address(self, address):
        self.address == address
    
5. test_is_homeless
    >       return address is None
    > NameError: name 'address' is not defined
    
        def is_homeless(self):
        '''
        returns True if address is not set, false in other case
        '''
        return address is None


    
 

