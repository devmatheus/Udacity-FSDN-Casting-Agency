class EntityCRUD {
    constructor(entityName, formId, listId, prevPageId, nextPageId) {
        this.entityName = entityName;
        this.form = document.getElementById(formId);
        this.list = document.getElementById(listId);
        this.prevPageButton = document.getElementById(prevPageId);
        this.nextPageButton = document.getElementById(nextPageId);
        this.page = 1;
        
        if (this.form) {
            this.form.addEventListener('submit', (event) => this.create(event));
        }

        if (this.prevPageButton) {
            this.prevPageButton.addEventListener('click', () => this.prevPage());
        }

        if (this.nextPageButton) {
            this.nextPageButton.addEventListener('click', () => this.nextPage());
        }
        
        this.fetchAndDisplay();
    }

    async fetchAndDisplay() {
        const entities = await this.fetchEntities();
        this.display(entities);
    }

    async fetchEntities() {
        const response = await fetch(`/api/${this.entityName}?page=${this.page}`);
        const data = await response.json();
        return data[this.entityName];
    }

    display(entities) {
        // To be implemented in the specific entity class (e.g., ActorCRUD, MovieCRUD)
    }

    async create(event) {
        event.preventDefault();
        const formData = this.getFormData();
        await fetch(`/api/${this.entityName}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });
        this.form.reset();
        this.fetchAndDisplay();
    }

    getFormData() {
        // To be implemented in the specific entity class (e.g., ActorCRUD, MovieCRUD)
    }

    async update(entityId, updatedData) {
        await fetch(`/api/${this.entityName}/${entityId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedData),
        });
        this.fetchAndDisplay();
    }

    async delete(entityId) {
        await fetch(`/api/${this.entityName}/${entityId}`, {
            method: 'DELETE',
        });
        this.fetchAndDisplay();
    }

    async nextPage() {
        this.page += 1;
        const entities = await this.fetchEntities();
        if (entities.length > 0) {
            this.display(entities);
        } else {
            this.page -= 1;
        }
    }

    async prevPage() {
        if (this.page > 1) {
            this.page -= 1;
            const entities = await this.fetchEntities();
            this.display(entities);
        }
    }
}

export { EntityCRUD };
