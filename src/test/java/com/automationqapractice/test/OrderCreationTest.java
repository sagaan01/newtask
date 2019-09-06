package com.automationqapractice.test;

import static org.testng.Assert.assertTrue;
import static org.testng.Assert.assertFalse;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

import com.automationqapractice.base.Dresscategory;
import com.automationqapractice.pages.AdressConfirmPage;
import com.automationqapractice.pages.FinalOrderConfirmPage;
import com.automationqapractice.pages.Homepage;
import com.automationqapractice.pages.LoginPage;
import com.automationqapractice.pages.OrderCompletionPage;
import com.automationqapractice.pages.OrderConfirmPage;
import com.automationqapractice.pages.PaymentConfirmPage;
import com.automationqapractice.pages.ProductConfirmPage;
import com.automationqapractice.pages.SearchresultsPage;
import com.automationqapractice.pages.ShippingConfirmPage;
import com.automationqapractice.pages.UserAccountPage;
import com.automationqapractice.utils.Userinfo;

public class OrderCreationTest extends TestBase {

    private static final Dresscategory PRINTED_SUMMER_DRESS = Dresscategory.PRINTED_SUMMER_DRESS;

    private Homepage homePage;
    private LoginPage signInPage;
    private UserAccountPage userAccountPage;
    private SearchresultsPage searchResultsPage;
    private ProductConfirmPage productConfirmationPage;
    private OrderConfirmPage orderConfirmationPage;
    private AdressConfirmPage confirmAddressesPage;
    private ShippingConfirmPage confirmShippingPage;
    private PaymentConfirmPage confirmPaymentPage;
    private FinalOrderConfirmPage finalConfirmationOnOrderPage;
    private OrderCompletionPage orderCompletionPage;
    private static Userinfo userInformation = Userinfo.getInstance();

    @BeforeClass(description = "Method Level Setup!")
    public void methodLevelSetup() {
        homePage = new Homepage(driver).get();
    }

    @Test
    public void purchaseProduct() throws InterruptedException {

        signInPage = homePage.clickSignInLink().get();

        userAccountPage = signInPage.signInWithRegisteredAccount(userInformation.getEmail(), userInformation.getPassword()).get();

        searchResultsPage = userAccountPage.searchFor(PRINTED_SUMMER_DRESS).get();

        assertTrue((searchResultsPage.getResultCount() > 0), "No Results found");

        productConfirmationPage = searchResultsPage.addToCart(PRINTED_SUMMER_DRESS).get();

        assertTrue(productConfirmationPage.isCorrectProductInformationDisplayedOnConfirmationDialogue(PRINTED_SUMMER_DRESS), "Product info not correct");

        orderConfirmationPage = productConfirmationPage.proceedToCheckout().get();

        assertTrue(orderConfirmationPage.isProductStillInStock(), "product out of stock");

        assertTrue(orderConfirmationPage.isCorrectProductQuantityAdded(), "wrong qty added");

        assertTrue(orderConfirmationPage.areDeliveryDetailsCorrect(), "wrong address details");

        confirmAddressesPage = orderConfirmationPage.checkout().get();

        assertTrue(confirmAddressesPage.isCorrectEmailSelected(), "Wrong email selected");

        confirmShippingPage = confirmAddressesPage.processAddress().get();

        if (!confirmShippingPage.isDefaultShippingSelected())
            confirmShippingPage.selectDefaultShipping();

        confirmShippingPage.agreeTermsOfService();

        confirmPaymentPage = confirmShippingPage.next().get();

        finalConfirmationOnOrderPage = confirmPaymentPage.payByCheck().get();

        orderCompletionPage = finalConfirmationOnOrderPage.submitOrder().get();

        assertTrue(orderCompletionPage.isOrderSuccessfullyPlaced(), "Order completion failed");
    }
}