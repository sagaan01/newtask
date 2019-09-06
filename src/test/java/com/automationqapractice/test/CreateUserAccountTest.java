package com.automationqapractice.test;

import static org.testng.Assert.assertEquals;

import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

import com.automationqapractice.pages.AccountCreationPage;
import com.automationqapractice.pages.Homepage;
import com.automationqapractice.pages.LoginPage;
import com.automationqapractice.pages.UserAccountPage;
import com.automationqapractice.utils.Userinfo;

public class CreateUserAccountTest extends TestBase{

		private Homepage homePage;
		private static Userinfo userInformation = Userinfo.getInstance();
		
		private LoginPage loginPage;
		private AccountCreationPage accountCreationPage;
		private UserAccountPage userAccountPage;
		
		@BeforeClass(description = "Method Level Setup!")
	    public void methodLevelSetup() {
	        homePage = new Homepage(driver).get();
	    }
		 
		@Test
		public void createNewUserAccount() {
			loginPage = homePage.clickSignInLink();
			loginPage.enterEmail(userInformation.getEmail());
				accountCreationPage = loginPage.submit();
				assertEquals(accountCreationPage.getEmailContent(), userInformation.getEmail(),  "Email not populated correctly");
				userAccountPage = accountCreationPage.fillForm(userInformation);
				userAccountPage.signOut();
		}
		
		@Test
		public void checkThatUserCanLoginSuccessfullyAfterAccountCreation() {
			loginPage = homePage.clickSignInLink();
			userAccountPage = loginPage.signInWithRegisteredAccount(userInformation.getEmail(), userInformation.getPassword());
			assertEquals(userAccountPage.userAccountInfo.getText(), userInformation.getFirstName() + " " + userInformation.getLastName(), "Could not login");
			userAccountPage.signOut();
		}
		
	}


