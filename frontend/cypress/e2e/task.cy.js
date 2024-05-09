describe('Task Creation Workflow', () => {
    let uid; // user id
    let email; // email of the user
    let Fullname;
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
                        todos: "watch video"
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
        // Enter the main page and login
        cy.visit('http://localhost:3000');
        cy.contains('div', 'Email Address').find('input[type=text]').type(email);
        cy.get('form').submit();
        // Click on the task to enter detail view
        cy.get('.title-overlay').click();
    });

    it('should allow adding a new todo item when description is provided', function() {
        cy.get('input[type=text]').type('New Todo');
        cy.get('input[type=submit]').click();

        cy.get('.todo-list').should('contain', 'New Todo');
    });

    it('should disable the add button when todo description is empty', function() {
        cy.get('input[type=text]').should('have.value', '');
        cy.get('input[type=submit]').should('be.disabled');
    });

    after(function () {
        // Clean up by deleting the user and task
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/tasks/${taskId}`
        });

        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`
        }).then((response) => {
            cy.log('User deleted:', response.body);
        });
    });
});