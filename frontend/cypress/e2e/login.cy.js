describe('Logging into the system', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  before(function () {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          email = user.email
        })
      })
  })

  beforeEach(function () {
    // enter the main main page
    cy.visit('http://localhost:3000')
  })

  it('starting out on the landing screen', () => {
    // make sure the landing page contains a header with "login"
    cy.get('h1')
      .should('contain.text', 'Login')
  })

  it('login to the system with an existing account', () => {
    // detect a div which contains "Email Address", find the input and type (in a declarative way)
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)
    // alternative, imperative way of detecting that input field
    //cy.get('.inputwrapper #email')
    //    .type(email)

    // submit the form on this page
    cy.get('form')
      .submit()

    // assert that the user is now logged in
    cy.get('h1')
      .should('contain.text', 'Your tasks, ' + name)
  })

  after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})



describe('Logging in and out from the system', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  before(function () {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          email = user.email
        })
      })
  })

  beforeEach(function () {
    // enter the main main page
    cy.visit('http://localhost:3000')
  })

  it('starting out on the landing screen', () => {
    // make sure the landing page contains a header with "login"
    cy.get('h1')
      .should('contain.text', 'Login')
  })

  it('login to the system with an existing account then out', () => {
    // detect a div which contains "Email Address", find the input and type (in a declarative way)
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)
    // alternative, imperative way of detecting that input field
    //cy.get('.inputwrapper #email')
    //    .type(email)

    // submit the form on this page
    cy.get('form')
      .submit()

    // assert that the user is now logged in
    cy.get('h1')
      .should('contain.text', 'Your tasks, ' + name)


      // Assuming the dropdown toggle has a class or ID that can be targeted
    cy.get('.icon-button').click(); // Open the dropdown
    cy.contains('Logout').click(); // Click on the logout
    cy.get('h1').should('contain.text', 'Login'); // Ensure the header still contains "Login"
  })


  after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})







describe('Signup towards the system', () => {
  let uid; // User id
  let name; // Name of the user (firstName + ' ' + lastName)
  let email; // Email of the user

  before(function () {
    cy.visit('http://localhost:3000');
    cy.contains('Have no account yet? Click here to sign up.').click();

    const randomNum = Date.now();
    const firstName = `Test${randomNum}`;
    const lastName = `User${randomNum}`;
    email = `test${randomNum}@example.com`;
    name = firstName + ' ' + lastName;

    cy.get('#firstname').type(firstName);
    cy.get('#lastname').type(lastName);
    cy.get('input[name="email"]').type(email);
    cy.get('form').submit();
  });


  it('should confirm the user is logged in after signup', () => {
    cy.get('h1').should('contain.text', `Your tasks, ${name}`);

   // Fetch the user by email
   cy.request('GET', `http://localhost:5000/users/bymail/${email}`)
   .then((response) => {
     console.log('Response Body:', response.body); // Log the entire response body to the console
     uid = response.body._id.$oid; // Correctly capture the MongoDB user ID
   });
});

  after(function () {
    if (uid) {
      cy.request('DELETE', `http://localhost:5000/users/${uid}`);
    }
  });
});



// describe('Login Process', () => {
//   before(() => {
//     cy.visit('http://localhost:3000');
//   });

//   it('should authenticate a user with valid credentials and redirect to task overview', () => {
//     cy.get('input[type="email"]').type('john.doe@example.com');
//     cy.get('input[type="password"]').type('password123');
//     cy.get('button[type="submit"]').click();
//     cy.url().should('include', '/tasks');
//     cy.contains('Your tasks');
//   });
// });



// describe('Login Process', () => {
//   before(() => {
//     cy.visit('http://localhost:3000');
//   });

//   it('should authenticate a user with valid credentials and redirect to task overview', () => {
//     cy.get('input[type="email"]').type('john.doe@example.com');
//     cy.get('input[type="password"]').type('password123');
//     cy.get('button[type="submit"]').click();
//     cy.url().should('include', '/tasks');
//     cy.contains('Your tasks');
//   });
// });