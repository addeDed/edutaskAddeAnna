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
        cy.get('input[type="text"][placeholder="Add a new todo item"]').type('New Todo');
        cy.get('input[type="submit"][value="Add"]').click();
        cy.get('.todo-list').should('contain', 'New Todo');
    });

    it('should toggle the status of the first todo item when clicked', function() {
        // Clicks the first toggle element
        cy.get('.todo-list .todo-item .checker').first().click();
        cy.wait(1000); // Wait for any asynchronous updates to complete
    
        // Check that the first checker has 'checked' class, indicating the item is "done"
        cy.get('.todo-list .todo-item .checker').first().should('have.class', 'checked');
    });
    
    it('should delete a todo item when delete icon is clicked', function() {
        cy.get('.todo-list .todo-item .remover').first().click(); // Clicks the delete icon of the first todo item.
        cy.get('.todo-list').should('not.contain', 'Initial Todo'); // Checks if the item is removed from the list.
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