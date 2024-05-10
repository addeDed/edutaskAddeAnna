describe('Task Creation Workflow', () => {
    let uid; // user id
    let email; // email of the user

    let taskId; // task id for cleanup
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
              email = user.email
             
                
              let data = {
                        title: "Cypress",
                        description: "Cypress Song",
                        url: "dQw4w9WgXcQ",
                        userid: uid,
                        todos: "watch video",
                    };
    
                    cy.request({
                        method: 'POST',
                        url: 'http://localhost:5000/tasks/create',
                        form: true,
                        body: data
                    })
            })
          })
      })

      beforeEach(function () {
        // Enter the main page
        cy.visit('http://localhost:3000')
        // Login
        cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(email)

        cy.get('form')
            .submit()
        // Should now be successfully logged in
        
        // Click on Task
        cy.get('.title-overlay').click()
        cy.wait(1000);
    })

    it('should allow adding a new todo item when description is provided', function() {
        
         // Precisely target the input field for new todo items by its placeholder
        cy.get('input[type="text"][placeholder="Add a new todo item"]').type('troll');  // Simulates typing 'troll' into the input field

         // Click the submit button by targeting it through its value attribute
        cy.get('input[type="submit"][value="Add"]').click();
       
    });


    after(function () {
        // Clean up by deleting the user and task
        
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`
        }).then((response) => {
            cy.log('User deleted:', response.body);
        });
    });
});