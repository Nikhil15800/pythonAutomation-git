from selenium.webdriver.common.by import By
from ..utils.baseClass import BaseClass
from ..config import Config
import random

class PlaceOrder(BaseClass):

    manCategory = (By.XPATH, "//a[normalize-space()='Men']")
    TSHIRT = (By.XPATH, "//a[normalize-space()='Tshirts']")
    categoryHeader = (By.XPATH, "//h2[contains(text(), 'Tshirts')]")
    totalproductOverlay = (By.XPATH, "//div[@class='single-products']")
    selectFirstProduct = (By.XPATH, "//a[@href='/product_details/2']")
    quantityField = (By.ID, 'quantity')
    addToCartButton = (By.XPATH, "//button[contains(@class,'btn btn-default cart')]")
    viewCartButton = (By.XPATH, "(//a[@href='/view_cart'])[2]")
    getTotalPrice = (By.XPATH, "//p[@class='cart_total_price']")
    productTitle = (By.XPATH, "//div[@class='product-information']//h2")
    viewProductPrice = (By.XPATH, "(//div[@class='product-information']//span)[2]")
    proceedCheckoutButton = (By.XPATH, "//a[normalize-space()='Proceed To Checkout']")
    placeOrderButton = (By.XPATH, "//a[contains(text(),'Place Order')]")
    nameOnCard = (By.XPATH, "//input[@class='form-control']")
    cardNumber = (By.XPATH, "//input[@data-qa='card-number']")
    cvcNumber = (By.XPATH, "//input[@name='cvc']")
    expirationMM = (By.XPATH, "//input[@name='expiry_month']")
    expirationYear = (By.XPATH,"//input[@name='expiry_year']")
    payOrderButton = (By.XPATH, "//button[@id='submit']")
    orderPlaceText = (By.XPATH, "//h2[@data-qa='order-placed']")
    popupHandle = (By.XPATH, "//div[@id='dismiss-button-element']")

    def __init__(self, driver):
        super().__init__(driver)

    def extractPriceValue(self, price_string):
        """Extract numeric value from price string like 'Rs. 800' -> '800'"""
        import re
        match = re.search(r'\d+', price_string)
        if match:
            return match.group()
        return price_string

    def selectManCategory(self):
        self.dismissAdPopupIfPresent()
        self.navigateToURL(Config.BASE_URL)
        self.logger.info("Navigated to home page before selecting category")
        self.dismissAdPopupIfPresent()
        self.waitForElement(*self.manCategory)
        self.clickElement(*self.manCategory)
        self.logger.info("Clicked on 'Men' category")   
        self.waitForElement(*self.TSHIRT)
        try:
            self.clickElement(*self.TSHIRT)
        except Exception:
            self.clickElementJS(*self.TSHIRT)

        self.logger.info("Clicked on 'Tshirts' subcategory")
        self.waitForElement(*self.categoryHeader)
        return self.getElementText(*self.categoryHeader)
    
    def getTotalProducts(self):
        self.waitForElement(*self.totalproductOverlay)
        products = self.driver.find_elements(*self.totalproductOverlay)
        self.logger.info(f"Total products found: {len(products)}")
        return len(products)
    
    def selectProduct(self):
        self.waitForElement(*self.selectFirstProduct)
        self.clickElement(*self.selectFirstProduct)
        self.logger.info("Selected the first product")

    def getProductDetails(self):
        self.waitForElement(*self.productTitle)
        self.productName = self.getElementText(*self.productTitle)
        viewProductPrice = self.getElementText(*self.viewProductPrice)
        self.productPrice = self.extractPriceValue(viewProductPrice)
        self.logger.info(f"Product Name: {self.productName}, Product Price: {self.productPrice}")
        return self.productName, self.productPrice
    
    def addToCart(self):
        self.getProductDetails()
        self.waitForElement(*self.addToCartButton)
        self.sendKeysJavaScript(*self.quantityField, "2")
        self.clickElement(*self.addToCartButton)
        self.logger.info("Clicked 'Add to cart' button")
        self.waitForElement(*self.viewCartButton)
        self.clickElement(*self.viewCartButton)
        self.logger.info("Clicked 'View Cart' button")

    def verifyCart(self):
        cartProductName = self.getElementText(By.XPATH, "//h4//a")
        cartProductPrice = self.getElementText(By.XPATH, "//td[@class='cart_price']//p")
        self.logger.info(f"Cart Product Name: {cartProductName}, Cart Product Price: {cartProductPrice}")
        self.logger.info(f"Verifying cart against stored details - Name: {self.productName}, Price: {self.productPrice}")
        assert self.productName in cartProductName, f"Expected product name to contain '{self.productName}', got '{cartProductName}'"
        assert self.productPrice in cartProductPrice, f"Expected product price to contain '{self.productPrice}', got '{cartProductPrice}'"
        self.logger.info("Cart verification successful")
        productTotalPrice = self.getElementText(*self.getTotalPrice)
        self.totalPrice = self.extractPriceValue(productTotalPrice)
        self.logger.info(f"Product Total Price (raw): {productTotalPrice}, Extracted value: {self.totalPrice}")
        expectedTotalPrice = str(int(self.productPrice) * 2)
        assert self.totalPrice == expectedTotalPrice, f"Expected total price to be '{expectedTotalPrice}', got '{self.totalPrice}'"

    def proceedCheckout(self):
        self.clickElement(*self.proceedCheckoutButton)
        self.logger.info("Click on the 'Procedd To Checckout' button")

    def placeOrder(self):
        self.clickElement(*self.placeOrderButton)
        self.logger.info("Click on the 'Place order' button")

    def payment(self):
        self.waitForElement(*self.nameOnCard)               
        self.sendKeysJavaScript(*self.nameOnCard, "John Doe")
        self.sendKeysJavaScript(*self.cardNumber, "4111111111111111")
        self.sendKeysJavaScript(*self.cvcNumber, "123")
        self.sendKeysJavaScript(*self.expirationMM, "12")
        self.sendKeys(*self.expirationYear, "2025")
        self.logger.info("Entered payment details")
        self.clickElement(*self.payOrderButton)
        self.logger.info("Clicked 'Pay and Confirm Order' button")
        self.waitForElement(*self.orderPlaceText)
        orderPlacedMessage = self.getElementText(*self.orderPlaceText)
        self.logger.info(f"Order placed message: {orderPlacedMessage}")
        assert "order placed!" in orderPlacedMessage.lower(), f"Expected order placed message to contain 'order placed!', got '{orderPlacedMessage.lower()}'"

        def dismissAdPopupIfPresent(self):
    
            self.switchToAlert()
            if self.isElementPresent(*self.popupHandle):
                self.popupHandle.click()
                self.logger.info("Dismissed ad popup using element click")
