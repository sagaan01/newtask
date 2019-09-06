package com.automationqapractice.pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.LoadableComponent;
import org.openqa.selenium.support.ui.WebDriverWait;

import com.automationqapractice.base.Dresscategory;

public class ProductConfirmPage extends LoadableComponent<ProductConfirmPage>{
	
	private WebDriver driver;
	private LoadableComponent<?> parent;
	
	public ProductConfirmPage(WebDriver driver, LoadableComponent<?> parent) {
		this.driver = driver;
		this.parent = parent;
		PageFactory.initElements(driver, this);
	}

	@Override
	protected void load() {
	}

	@Override
	protected void isLoaded() throws Error {
			new WebDriverWait(driver, 5).until(ExpectedConditions.elementToBeClickable(productCardElement));
	}
	
	@FindBy (className = "layer_cart_product")
	public WebElement productCardElement;
	
	@FindBy (id = "layer_cart_product_title")
	public WebElement productInfoElement;
	
	@FindBy (xpath = "//a[@title='Proceed to checkout']")
	public WebElement checkoutButtonElement;

	public boolean isProductConfirmationDisplayed() {
		return productCardElement.getAttribute("innerText").contains("Product successfully added to your shopping cart");
	}
	
	public <DressCategory> boolean isCorrectProductInformationDisplayedOnConfirmationDialogue(Dresscategory dress) {
		return isProductConfirmationDisplayed() && productInfoElement.getAttribute("innerText").trim().equalsIgnoreCase(dress.getName());
	}
	
	public OrderConfirmPage proceedToCheckout() {
		checkoutButtonElement.click();
		return new OrderConfirmPage(driver, this);
	}

	
}