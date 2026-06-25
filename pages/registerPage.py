from selenium.webdriver.common.by import By
from ..utils.baseClass import BaseClass
import time

class Register(BaseClass):

    genderField = (By.ID, 'id_gender1')
    accountCreate = (By.XPATH, "//b[normalize-space()='Account Created!']")

    def __init__(self, driver):
        super().__init__(driver)

    def goToRegisterPage(self):
        self.logger.info("Navigating to register page")
        self.clickElement(By.LINK_TEXT, "Signup / Login")
        
    def register(self, name, email):
        self.logger.info(f"Registering user: {name}, {email}")
        self.waitForElement(By.NAME, "name")
        self.sendKeys(By.XPATH, "//input[@type='text']", name)
        self.sendKeys(By.XPATH, "//input[@data-qa='signup-email']", email)
        self.clickElement(By.XPATH, "//button[@type='submit'  and @data-qa='signup-button']")
        self.logger.info("Registration form submitted")

    def enterAccountInformation(self,password, day, month, year, firstName, lastName, company, address1, address2, country, state, city, zipcode, mobileNumber):
        self.logger.info("Entering account information")
        self.waitForElement(*self.genderField)
        self.clickElement(*self.genderField)
        self.sendKeys(By.ID, "password", password)
        self.waitForElement(By.ID, "days")
        self.clickElement(By.XPATH, f"//select[@id='days']/option[@value='{day}']")
        self.waitForElement(By.ID, "months")
        self.clickElement(By.XPATH, f"//select[@id='months']/option[@value='{month}']")
        self.waitForElement(By.ID, "years")
        self.clickElement(By.XPATH, f"//select[@id='years']/option[@value='{year}']")
        self.sendKeys(By.ID, "first_name", firstName)
        self.sendKeys(By.ID, "last_name", lastName)
        self.sendKeys(By.ID, "company", company)
        self.sendKeys(By.ID, "address1", address1)
        self.sendKeys(By.ID, "address2", address2)
        self.waitForElement(By.ID, "country")
        self.clickElement(By.XPATH, f"//select[@id='country']/option[text()='{country}']")
        self.sendKeys(By.ID, "state", state)
        self.sendKeys(By.ID, "city", city)
        self.sendKeys(By.ID, "zipcode", zipcode)
        self.sendKeys(By.ID, "mobile_number", mobileNumber)
        self.clickElement(By.XPATH, "//button[@type='submit']")
        self.logger.info("Account information submitted")
        self.logger.info(f"Current URL after submit: {self.getCurrentURL()}")
        self.logger.info(f"Page title after submit: {self.getTitle()}")


    def verifyAccountCreated(self):
        self.waitForElement(*self.accountCreate)
        getAccountText = self.getElementText(*self.accountCreate)
        self.clickElement(By.XPATH, "//a[@data-qa='continue-button']")
        return getAccountText