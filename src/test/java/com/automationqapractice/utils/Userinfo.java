package com.automationqapractice.utils;
import com.github.javafaker.Faker;
import com.github.javafaker.service.FakeValuesService;
import com.github.javafaker.service.RandomService;
import java.util.Locale;

public class Userinfo {
	
		
		private static Userinfo userInformation;

		private Userinfo() {
			
		}
		
		private String firstName;
		private String lastName;
		private String password;
		private String company;
		private String address;
		private String city;
		private String state;
		private String zipcode;
		private String alias;
		private String mobileNumber;
		private String email;
		private String country;
		
		public static class Builder{
			
			private String firstName;
			private String lastName;
			private String password;
			private String company;
			private String address;
			private String city;
			private String state;
			private String zipcode;
			private String alias;
			private String mobileNumber;
			private String email;
			private String country;
			
			public Builder (String firstName) {
				this.firstName = firstName;
			}
			
			public Builder withLastName(String lastName) {
				this.lastName = lastName;
				return this;
			}
			
			public Builder passwordAs(String password) {
				this.password = password;
				return this;
			}
			
			public Builder worksAtCompany(String company) {
				this.company = company;
				return this;
			}
			
			public Builder livesAt(String address) {
				this.address = address;
				return this;
			}
			
			public Builder in(String city) {
				this.city = city;
				return this;
			}
			
			public Builder inState(String state) {
				this.state = state;
				return this;
			}
			
			public Builder withZipCode(String zipcode) {
				this.zipcode = zipcode;
				return this;
			}
			
			public Builder andAlias(String alias) {
				this.alias = alias;
				return this;
			}
			
			public Builder andEmail(String email) {
				this.email = email;
				return this;
			}
			
			public Builder withMobileNumber(String mobileNumber) {
				this.mobileNumber = mobileNumber;
				return this;
			}
			
			public Builder inCountry(String country) {
				// TODO Auto-generated method stub
				this.country = country;
				return this;
			}
			
			public Userinfo build() {
				Userinfo userInformation = new Userinfo();
				userInformation.address = this.address;
				userInformation.firstName = this.firstName;
				userInformation.lastName = this.lastName;
				userInformation.password = this.password;
				userInformation.company = this.company;
				userInformation.alias = this.alias;
				userInformation.state = this.state;
				userInformation.zipcode = this.zipcode;
				userInformation.city = this.city;
				userInformation.mobileNumber = this.mobileNumber;
				userInformation.email = this.email;
				userInformation.country = this.country;
				return userInformation;
			}

		}

		public String getFirstName() {
			return this.firstName;
		}
		
		public String getLastName() {
			return this.lastName;
		}
		
		public String getPassword() {
			return this.password;
		}

		public String getCompany() {
			return company;
		}

		public void setCompany(String company) {
			this.company = company;
		}

		public String getAddress() {
			return address;
		}

		public void setAddress(String address) {
			this.address = address;
		}

		public String getCity() {
			return city;
		}

		public void setCity(String city) {
			this.city = city;
		}

		public String getState() {
			return state;
		}

		public void setState(String state) {
			this.state = state;
		}

		public String getZipcode() {
			return zipcode;
		}

		public void setZipcode(String zipcode) {
			this.zipcode = zipcode;
		}

		public String getAlias() {
			return alias;
		}

		public void setAlias(String alias) {
			this.alias = alias;
		}

		public void setPassword(String password) {
			this.password = password;
		}
		
		public String getMobileNumber() {
			return mobileNumber;
		}
		
		public String getEmail() {
			return email;
		}
		
		public String getCountry() {
			return country;
		}
		
		@Override
		public String toString() {
			return getAddress() + getAlias() + getCity() + getCompany() + getEmail() + getFirstName() + getLastName() + getMobileNumber()
			+ getPassword() + getState() + getZipcode() + getZipcode();
		}
		
		public static Userinfo creatUserInformation() {
			Faker faker = new Faker(new Locale("en-US"));
			FakeValuesService fakeValuesService = new FakeValuesService(new Locale("en-US"), new RandomService());
			String email = fakeValuesService.bothify("????##@gmail.com");
			String zipCode = fakeValuesService.bothify("#####");
			Userinfo data = new Userinfo.Builder(faker.name().firstName())
					.withLastName(faker.name().lastName())
					.passwordAs(fakeValuesService.bothify("password##"))
					.livesAt(faker.address().buildingNumber()+ faker.address().streetAddress())
					.in(faker.address().cityName())
					.inCountry("United States")
					.withMobileNumber(faker.phoneNumber().cellPhone())
					.andAlias(fakeValuesService.bothify("????##@gmail.com"))
					.withZipCode(zipCode)
					.andEmail(email)
					.worksAtCompany(faker.company().name())
					.build();
			return data;
		}
		
		  public static Userinfo getInstance() {
		        if (userInformation == null)
		            createInstance();
		        return userInformation;
		    }
		  
		  public static Userinfo createInstance() {
			  userInformation = creatUserInformation();
			  return userInformation;
		    }
		
	}


