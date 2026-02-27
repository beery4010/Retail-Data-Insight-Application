from Core.data_loader import *
from Core.logger import *
from Core.report_generator import ReportGenerator

logger = Logger().setup_logs()

class RetailApp:
    def __init__(self):
        self.choic_menu()

    def choic_menu(self):
        try:
            with open("user_instruction.txt","r") as file:
                user_instruction = file.read()
            user_instruction = user_instruction.split("\n;\n")[0]
        except Exception as e:
            print(f"Got Error in Reading the User Instruction File: {e}")
            logger.error(f"Got Error in Reading the User Instruction File: {e}")
        else: 
            try:
                user_input = int(input(user_instruction))
                logger.info(f"User has Selected: {user_input}")
                match user_input:
                    case 1:
                        logger.info("Generating the Level 1 Report")
                        print("Generating the Level 1 Report, Please Wait.")
                        data = DataLoader()
                        level_1_data = data._handle_level_1()
                        ReportGenerator(user_input, level_1_data)
                        print("Generated the Level 1 Report, Please Check in the Application Folder.")
                        logger.info("Generated the Level 1 Report")
                    case 2:
                        logger.info("Generating the Level 2 Report")
                        print("Generating the Level 2 Report, Please Wait.")
                        data = DataLoader()
                        level_1_data = data._handle_level_1()
                        level_2_data = data._handle_level_2()
                        ReportGenerator(user_input, level_1_data, level_2_data)
                        print("Generated the Level 2 Report, Please Check in the Application Folder.")
                        logger.info("Generated the Level 2 Report")
                    case 3:
                        logger.info("Generating the Level 3 Report")
                        print("Generating the Level 3 Report, Please Wait.")
                        data = DataLoader()
                        level_1_data = data._handle_level_1()
                        level_2_data = data._handle_level_2()
                        level_3_data = data._handle_level_3()
                        ReportGenerator(user_input, level_1_data, level_2_data, level_3_data)
                        print("Generated the Level 3 Report, Please Check in the Application Folder.")
                        logger.info("Generated the Level 3 Report")
                    case _:
                        print("Closing the Application")
                        logger.info("Closing the Application")
                        sys.exit()
            except Exception as e:
                print(f"Got Error in getting the user input or processing the data: {e}")
                logger.error(f"Got Error in getting the user input or processing the data: {e}")
                



if __name__ == "__main__":
    RetailApp()