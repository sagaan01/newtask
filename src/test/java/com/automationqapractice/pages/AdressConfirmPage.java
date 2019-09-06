package com.automationqapractice.pages;

import static org.testng.Assert.assertTrue;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.LoadableComponent;
import org.openqa.selenium.support.ui.Select;

import com.automationqapractice.utils.Userinfo;

public class AdressConfirmPage extends LoadableComponent<AdressConfirmPage>{

	private WebDriver driver;
	@SuppressWarnings("unused")
	private LoadableComponent<OrderConfirmPage> OrderConfirmPage;
	Userinfo userInformation = Userinfo.getInstance();
	
	public AdressConfirmPage(WebDriver driver, LoadableComponent<OrderConfirmPage> OrderConfirmPage) {
		this.driver = driver;
		this.OrderConfirmPage = OrderConfirmPage;
		PageFactory.initElements(driver, this);
	}

	@FindBy (css = ".step_current")
	public WebElement selectedSection;
	
	@FindBy(css = "select#id_address_delivery")
	public WebElement selectAddressElement;
	
	@FindBy(name = "processAddress")
	public WebElement processAddress;
	
	@Override
	protected void load() {
	}

	@Override
	protected void isLoaded() throws Error {
		assertTrue(selectedSection.getAttribute("innerText").trim().contains("Address"), "Not on correct page");
	}
	
	public boolean isCorrectEmailSelected() {
		Select select = new Select(selectAddressElement);
		return select.getFirstSelectedOption().getAttribute("innerText").trim().equalsIgnoreCase(userInformation.getAlias());
	}
	
	public ShippingConfirmPage processAddress() {
		processAddress.click();
		return new ShippingConfirmPage(driver, this);
	}

}