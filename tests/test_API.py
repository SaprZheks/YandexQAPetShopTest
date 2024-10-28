import requests
import json
import os
import pytest



class TestPet:
    test_files_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_files',
    )
    common_url = "https://petstore.swagger.io/v2"
    
    @pytest.mark.parametrize(
            "var_id, var_category_id, var_category_name, var_name, var_photoUrls, var_tags, var_status, expected_status_code",
        [
            # Негативные тесты
            ("string", 666, "ChelMedvedoSvin", "ShizoMonster Andrey", ["string 1"],
             [{"id":13, "name": "some name"}], "available", 500),
            (777777, "string", "ChelMedvedoSvin", "ShizoMonster Andrey", ["string 1"],
             [{"id":13, "name": "some name"}], "available", 500),
            (777777, 666, ["ChelMedvedoSvin"], "ShizoMonster Andrey", ["string 1"],
             [{"id":13, "name": "some name"}], "available", 500),
            (777777, 666, "ChelMedvedoSvin", ["ShizoMonster Andrey"], ["string 1"],
             [{"id":13, "name": "some name"}], "available", 500),
            (777777, 666, "ChelMedvedoSvin", "ShizoMonster Andrey", "string 1",
             [{"id":13, "name": "some name"}], "available", 500),
            (777777, 666, "ChelMedvedoSvin", "ShizoMonster Andrey", ["string 1"],
             [{"id":"string", "name": "some name"}], "available", 500),
            (777777, 666, "ChelMedvedoSvin", "ShizoMonster Andrey", ["string 1"],
             [{"id":13, "name": ["some name"]}], "available", 500),
            (777777, 666, "ChelMedvedoSvin", "ShizoMonster Andrey", ["string 1"],
             ["id"], "available", 500),
            (777777, 666, "ChelMedvedoSvin", "ShizoMonster Andrey", ["string 1"],
             [5], "available", 500),
            (777777, 666, "ChelMedvedoSvin", "ShizoMonster Andrey", ["string 1"],
             {"id":13, "name": "some name"}, "available", 500),
            (777777, 666, "ChelMedvedoSvin", "ShizoMonster Andrey", ["string 1"],
             [{"id":13, "name": "some name"}], "some alien string", 500),
            (777777, 666, "ChelMedvedoSvin", "ShizoMonster Andrey", ["string 1"],
             [{"id":13, "name": "some name"}], ["some alien string"], 500),
            # Позитивные тесты
            (777777, 666, "ChelMedvedoSvin", "ShizoMonster Andrey", ["string 1"],
             [{"id":13, "name": "some name"}], "available", 200),
            (777777, 666, "ChelMedvedoSvin", "ShizoMonster Andrey", ["string 1","string 2"],
             [{"id":13, "name": "some name"}], "available", 200),
            (777777, 666, "ChelMedvedoSvin", "ShizoMonster Andrey", ["string 1"],
             [{"id":13, "name": "some name"},{"id":14, "name": "some name 2"}], "available", 200),
            (777777, 666, "ChelMedvedoSvin", "ShizoMonster Andrey", ["string 1"],
             [{"id":13, "name": "some name"}], "pending", 200),
            (777777, 666, "ChelMedvedoSvin", "ShizoMonster Andrey", ["string 1"],
             [{"id":13, "name": "some name"}], "sold", 200)
        ]
    )
    def test_POST_Add_new_pet(self, var_id, var_category_id, var_category_name, var_name, var_photoUrls, var_tags, var_status, expected_status_code): # Добавление нового питомца
        url = self.common_url + "/pet"

        headers = {
            'Content-Type': 'application/json'
        }

        payload = json.dumps({
            "id": var_id,  # integer
            "category": {
                "id": var_category_id, # integer
                "name": var_category_name # string
            },
            "name": var_name, # string
            "photoUrls": var_photoUrls, # list of strings
            "tags": var_tags, # list of dicts {id: integer, name: string}
            "status": var_status # enum string: available, pending, sold
        })

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.status_code)
        print(response.json)

        assert response.status_code == expected_status_code

    @pytest.mark.parametrize(
        "var_status, expected_status_code",
        [
            # Негативные тесты
            ("random text",500),
            # Позитивные тесты
            ("available",200),
            ("pending",200),
            ("sold",200),
            ("available,pending",200),
            ("available,sold",200),
            ("pending,sold",200),
            ("available,pending,sold",200)
        ]
    )
    def test_GET_Find_pets_by_status(self,var_status, expected_status_code):
        url = self.common_url + "/pet/findByStatus?status="+var_status # string

        payload = {}

        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.status_code)
        print(response.json)

        assert response.status_code == expected_status_code

    @pytest.mark.parametrize(
        "var_id, expected_status_code",
        [
            # Негативные тесты
            ("some random text",404),
            ("[777777]",404),
            # Позитивные тесты
            (777777,200)
        ]
    )
    def test_GET_Find_pet_by_ID(self,var_id,expected_status_code):
        url = self.common_url + "/pet/"+str(var_id)

        payload = {}

        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.status_code)
        print(response.json)

        assert response.status_code == expected_status_code

    @pytest.mark.parametrize(
        "var_id, var_Metadata, var_image_name, expected_status_code",
        [
            # Негативные тесты
            ("some random text","some string 1234",r"\chel_medvedo_svin.jpg", 404),
            # Позитивные тесты
            (777777,"",r"\chel_medvedo_svin.jpg", 200),
            (777777,"some string 1234",r"\chel_medvedo_svin.jpg", 200),
            (777777,"some string 1234",r"\chel_medvedo_svin.png", 200)
        ]
    )
    def test_POST_Upload_photo_of_pet_by_ID(self,var_id,var_Metadata, var_image_name, expected_status_code):
        url = self.common_url + "/pet/"+str(var_id)+"/uploadImage"

        payload = {'additionalMetadata': var_Metadata}

        files= {'file': open(self.test_files_path + var_image_name, 'rb')}

        headers = {}
        
        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        print(response.status_code)
        print(response.json)

        assert response.status_code == expected_status_code

    @pytest.mark.parametrize(
        "var_id, var_name, var_status, expected_status_code",
        [
            # Негативные тесты
            ("some random text","Chuvachela%20Bro","sold", 404),
            # Позитивные тесты
            (777777,"Chuvachela%20Bro","sold", 200)
        ]
    )
    def test_POST_change_pets_data_by_ID(self, var_id, var_name, var_status, expected_status_code):

        url = self.common_url + "/pet/" + str(var_id)
        
        payload = 'name='+var_name+'&status='+var_status

        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.status_code)
        print(response.json)

        assert response.status_code == expected_status_code

    @pytest.mark.parametrize(
        "var_id, var_api_key, expected_status_code",
        [
            # Негативные тесты
            ("some random text",'special-key', 404),
            # Позитивные тесты
            (777777,'special-key', 200),
            (777777,'special-key', 404) # После удаления он его не обнаружит
        ]
    )
    def test_DELETE_pet_by_ID(self, var_id, var_api_key, expected_status_code):

        url = self.common_url + "/pet/" + str(var_id)

        payload = {}

        headers = {
        'api_key': var_api_key
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)

        print(response.status_code)
        print(response.json)

        assert response.status_code == expected_status_code



class TestOrder:
    test_files_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_files',
    )
    common_url = "https://petstore.swagger.io/v2"
    
    @pytest.mark.parametrize(
        "var_id, var_petId, var_quantity, var_shipDate, var_status, var_complete, expected_status_code",
        [
            # Негативные тесты
            ("some string",0,1,"2024-10-28T03:36:14.769Z","placed",True,500),
            (0,"some string",1,"2024-10-28T03:36:14.769Z","placed",True,500),
            (0,0,"some string","2024-10-28T03:36:14.769Z","placed",True,500),
            (0,0,1,"random text","placed",False,500),
            (0,0,1,"2024-10-28T03:36:14.769Z","not in enum list text",False,500),
            # Позитивные тесты
            (7,0,1,"2024-10-28T03:36:14.769Z","placed",False,200),
            (7,0,1,"2024-10-28T03:36:14.769Z","placed",True,200),
            (7,0,1,"2024-10-28T03:36:14.769Z","approved",True,200),
            (7,0,1,"2024-10-28T03:36:14.769Z","delivered",True,200),
        ]
    )
    def test_POST_Add_new_order(self, var_id, var_petId, var_quantity, var_shipDate, var_status, var_complete, expected_status_code):
        url = self.common_url + "/store/order"

        headers = {
            'Content-Type': 'application/json'
        }

        payload = json.dumps({
            "id": var_id, # integer
            "petId": var_petId, # integer
            "quantity": var_quantity, # integer
            "shipDate": var_shipDate, # string date
            "status": var_status, # string enum from [placed, approved, delivered]
            "complete": var_complete # booleand
        })

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.status_code)
        print(response.json)

        assert response.status_code == expected_status_code
    
    @pytest.mark.parametrize(
        "var_id, expected_status_code",
        [
            # Негативные тесты
            ("random string", 404),
            # Позитивные тесты
            (7, 200)
        ]
    )
    def test_GET_Get_order_by_ID(self, var_id, expected_status_code):
        url = self.common_url + "/store/order/" + str(var_id)

        headers = {}

        payload = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.status_code)
        print(response.json)

        assert response.status_code == expected_status_code

    @pytest.mark.parametrize(
        "expected_status_code",
        [
            # Позитивные тесты
            (200)
        ]
    )
    def test_GET_Get_inventory(self, expected_status_code):
        url = self.common_url + "/store/inventory"

        headers = {}

        payload = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.status_code)
        print(response.json)

        assert response.status_code == expected_status_code

    @pytest.mark.parametrize(
        "var_id, expected_status_code",
        [
            # Негативные тесты
            ("random text",404),
            # Позитивные тесты
            (7, 200)
        ]
    )
    def test_DELETE_Delete_by_ID(self, var_id, expected_status_code):
        url = self.common_url + "/store/order/" + str(var_id)

        headers = {
            'api_key': 'special-key'
        }

        payload = {}

        response = requests.request("DELETE", url, headers=headers, data=payload)

        print(response.status_code)
        print(response.json)

        assert response.status_code == expected_status_code


class TestUser:
    test_files_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_files',
    )
    common_url = "https://petstore.swagger.io/v2"
    
    @pytest.mark.parametrize(
        "var_list_of_dicts, expected_status_code",
        [
            # Негативные тесты
            ([("string","SaprZheks","Zheks","Sapr","SaprZheks@gmail.com","passwd","89998887766",0)],500),
            ([(17,"SaprZheks","Zheks","Sapr","SaprZheks@gmail.com","passwd","89998887766","string")],500),
            ((17,"SaprZheks","Zheks","Sapr","SaprZheks@gmail.com","passwd","89998887766",0),500),
            # Позитивные тесты
            (
                [(17,"SaprZheks","Zheks","Sapr","SaprZheks@gmail.com","passwd","89998887766",0)],
                200
            ),
            
            (
                [
                    (17,"SaprZheks","Zheks","Sapr","SaprZheks@gmail.com","passwd","89998887766",0),
                    (18,"SaprZheks","Zheks","Sapr","SaprZheks@gmail.com","passwd","89998887766",0)
                ],
                200
            )
        ]
    )
    def test_POST_Create_list_of_users_from_list(self, var_list_of_dicts, expected_status_code): 
        url = self.common_url + "/user/createWithList"

        headers = {
            'Content-Type': 'application/json'
        }
        json_list = ["id","username","firstName","lastName","email","password","phone","userStatus"]
        if isinstance(var_list_of_dicts,tuple):
            dictionary = {}
            for i in range(len(json_list)):
                dictionary[json_list[i]] = var_list_of_dicts[i]
            payload = json.dumps(
                dictionary
            )
        elif isinstance(var_list_of_dicts,list):
            list_of_dicts = []
            for i in range(len(var_list_of_dicts)):
                dictionary = {}
                for j in range(len(json_list)):
                    dictionary[json_list[j]] = var_list_of_dicts[i][j]
                list_of_dicts.append(dictionary)
            
            payload = json.dumps(
                list_of_dicts
            )
        
        

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.status_code)
        print(response.json)

        assert response.status_code == expected_status_code
    
    @pytest.mark.parametrize(
        "var_list_of_dicts, expected_status_code",
        [
            # Негативные тесты
            ([("string","SaprZheks","Zheks","Sapr","SaprZheks@gmail.com","passwd","89998887766",0)],500),
            ([(17,"SaprZheks","Zheks","Sapr","SaprZheks@gmail.com","passwd","89998887766","string")],500),
            # Позитивные тесты
            (
                [(17,"SaprZheks","Zheks","Sapr","SaprZheks@gmail.com","passwd","89998887766",0)],
                200
            ),
            
            (
                [
                    (17,"SaprZheks","Zheks","Sapr","SaprZheks@gmail.com","passwd","89998887766",0),
                    (18,"SaprZheks2","Zheks","Sapr","SaprZheks@gmail.com","passwd","89998887766",0)
                ],
                200
            )
        ]
    )
    def test_POST_Create_list_of_users_from_array(self, var_list_of_dicts, expected_status_code): 
        url = self.common_url + "/user/createWithArray"

        headers = {
            'Content-Type': 'application/json'
        }
        json_list = ["id","username","firstName","lastName","email","password","phone","userStatus"]
        if isinstance(var_list_of_dicts,tuple):
            dictionary = {}
            for i in range(len(json_list)):
                dictionary[json_list[i]] = var_list_of_dicts[i]
            payload = json.dumps(
                dictionary
            )
        elif isinstance(var_list_of_dicts,list):
            list_of_dicts = []
            for i in range(len(var_list_of_dicts)):
                dictionary = {}
                for j in range(len(json_list)):
                    dictionary[json_list[j]] = var_list_of_dicts[i][j]
                list_of_dicts.append(dictionary)
            
            payload = json.dumps(
                list_of_dicts
            )
        
        

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.status_code)
        print(response.json)

        assert response.status_code == expected_status_code

    @pytest.mark.parametrize(
        "var_id, var_username, var_firstName, var_lastName, var_email, var_password, var_phone, var_userStatus, wrapper, expected_status_code",
        [
            # Негативные тесты
            ("string","SaprZheks","Zheks","Sapr","SaprZheks@gmail.com","passwd","89998887766",0,None, 500),
            (17,"SaprZheks","Zheks","Sapr","SaprZheks@gmail.com","passwd","89998887766","string",None, 500),
            (17,"SaprZheks","Zheks","Sapr","SaprZheks@gmail.com","passwd","89998887766",0,'[]', 500),

            # Позитивные тесты
            (17,"SaprZheks","Zheks","Sapr","SaprZheks@gmail.com","passwd","89998887766",0,None, 200)
        ]
    )
    def test_POST_Create_user(self, var_id, var_username, var_firstName, var_lastName, var_email, var_password, var_phone, var_userStatus, wrapper, expected_status_code): 
        url = self.common_url + "/user"

        headers = {
            'Content-Type': 'application/json'
        }
        if wrapper == '[]':
            payload = json.dumps(
                [{
                    "id": var_id,
                    "username": var_username,
                    "firstName": var_firstName,
                    "lastName": var_lastName,
                    "email": var_email,
                    "password": var_password,
                    "phone": var_phone,
                    "userStatus": var_userStatus
                }]
            )
        elif wrapper == None:
            payload = json.dumps(
                {
                    "id": var_id,
                    "username": var_username,
                    "firstName": var_firstName,
                    "lastName": var_lastName,
                    "email": var_email,
                    "password": var_password,
                    "phone": var_phone,
                    "userStatus": var_userStatus
                }
            )
        
        

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.status_code)
        print(response.json)

        assert response.status_code == expected_status_code

    @pytest.mark.parametrize(
        "var_username, expected_status_code",
        [
            # Негативные тесты
            ("SaprZheks_404", 404),
            # Позитивные тесты
            ("SaprZheks", 200)
        ]
    )
    def test_GET_Get_user_by_username(self, var_username, expected_status_code): 
        url = self.common_url + "/user/" + str(var_username)

        headers = {}
        
        payload = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.status_code)
        print(response.json)

        assert response.status_code == expected_status_code

    @pytest.mark.parametrize(
        "var_params, expected_status_code",
        [
            # Позитивные тесты
            ("",200),
            ("?username=SaprZheks_404&password=passwd", 200),
            ("?username=SaprZheks&password=notpassword", 200),
            ("?username=SaprZheks", 200),
            ("?password=passwd", 200),
            ("?password=notpassword", 200),
            ("?username=SaprZheks&password=passwd", 200)
        ]
    )
    def test_GET_Login_user(self, var_params, expected_status_code): 
        url = self.common_url + "/user/login" + str(var_params)

        headers = {}
        
        payload = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.status_code)
        print(response.json)

        assert response.status_code == expected_status_code

    @pytest.mark.parametrize(
        "var_id, var_username, var_firstName, var_lastName, var_email, var_password, var_phone, var_userStatus, expected_status_code",
        [
            # Негативные тесты
            ("string","SaprZheks new","Zheks new","Sapr new","SaprZheksNew@gmail.com","passwdNew","89998887700",1, 500),
            (17,"SaprZheks new","Zheks new","Sapr new","SaprZheksNew@gmail.com","passwdNew","89998887700","string", 500),
            # Позитивные тесты
            (17,"SaprZheks new","Zheks new","Sapr new","SaprZheksNew@gmail.com","passwdNew","89998887700", 1, 200)
        ]
    )
    def test_PUT_Update_user(self, var_id, var_username, var_firstName, var_lastName, var_email, var_password, var_phone, var_userStatus, expected_status_code): 
        url = self.common_url + "/user/" + str(var_username)

        headers = {
            'Content-Type': 'application/json'
        }
        
        payload = json.dumps(
            {
                "id": var_id,
                "username": var_username,
                "firstName": var_firstName,
                "lastName": var_lastName,
                "email": var_email,
                "password": var_password,
                "phone": var_phone,
                "userStatus": var_userStatus
            }        
        )

        response = requests.request("PUT", url, headers=headers, data=payload)

        print(response.status_code)
        print(response.json)

        assert response.status_code == expected_status_code
    
    @pytest.mark.parametrize(
        "expected_status_code",
        [
            # Позитивные тесты
            (200)
        ]
    )
    def test_GET_Logout_user(self, expected_status_code): 
        url = self.common_url + "/user/logout"

        headers = {}
        
        payload = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.status_code)
        print(response.json)

        assert response.status_code == expected_status_code
    
    @pytest.mark.parametrize(
        "var_user, expected_status_code",
        [
            # Негативные тесты
            ("",405),
            ("NoSaprZheks",404),
            ("SaprZheks",404),
            # Позитивные тесты
            ("SaprZheks new",200)
        ]
    )
    def test_DELETE_Delete_user(self, var_user, expected_status_code): 
        url = self.common_url + "/user/" + str(var_user)

        headers = {}
        
        payload = {}

        response = requests.request("DELETE", url, headers=headers, data=payload)

        print(response.status_code)
        print(response.json)

        assert response.status_code == expected_status_code