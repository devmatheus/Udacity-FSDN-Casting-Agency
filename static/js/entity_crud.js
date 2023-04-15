import { getIdFromUrl } from './utils.js';

class EntityCRUD {
    constructor(entityName, formId, listId, prevPageId, nextPageId) {
        this.entityName = entityName;
        this.form = document.getElementById(formId);
        this.list = document.getElementById(listId);
        this.prevPageButton = document.getElementById(prevPageId);
        this.nextPageButton = document.getElementById(nextPageId);
        this.page = 1;

        if (this.form) {
            this.form.addEventListener('submit', (e) => crudInstance.save(e));
        }

        if (this.prevPageButton) {
            this.prevPageButton.addEventListener('click', () => this.prevPage());
        }

        if (this.nextPageButton) {
            this.nextPageButton.addEventListener('click', () => this.nextPage());
        }

        const editId = getIdFromUrl(this.entityName);
        if (editId) {
            const ctrl = this;
            this.fetchEntity(editId)
                .then((entity) => {
                    ctrl.populateForm(entity.data);
                });
        }

        if (this.list) {
            this.fetchAndDisplay();
        }
    }

    async fetchAndDisplay() {
        const paginate = await this.paginate();
        const entities = paginate[this.entityName];
        this.display(entities);
        this.disablePaginationButtons(paginate);
    }

    async paginate() {
        const response = await fetch(`/api/${this.entityName}?page=${this.page}`, {
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
            },
        });
        return await response.json();
    }

    async fetchEntities() {
        const paginate = await this.paginate();
        return paginate[this.entityName];
    }

    async fetchEntity(entityId) {
        const response = await fetch(`/api/${this.entityName}/${entityId}`, {
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
            },
        });
        const data = await response.json();
        return data;
    }

    display(entities) {
        // To be implemented in the specific entity class (e.g., ActorCRUD, MovieCRUD)
    }

    async create() {
        const formData = this.getFormData();
        await fetch(`/api/${this.entityName}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
            },
            body: JSON.stringify(formData),
        });
        this.form.reset();
        window.location.href = `/${this.entityName}`;
    }

    getFormData() {
        // To be implemented in the specific entity class (e.g., ActorCRUD, MovieCRUD)
    }

    async edit(id) {
        window.location.href = `/${this.entityName}/${id}/edit`;
    }

    populateForm(item) {
        for (const key in item) {
            const input = document.getElementById(key);
            if (input) {
                input.value = item[key];
            }
        }
    }

    save(event) {
        event.preventDefault();
        const entityId = getIdFromUrl(this.entityName);
        if (entityId) {
            this.update(entityId, this.getFormData());
        } else {
            this.create();
        }
        return false;
    }

    async update(entityId, updatedData) {
        await fetch(`/api/${this.entityName}/${entityId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
            },
            body: JSON.stringify(updatedData),
        });
        window.location.href = `/${this.entityName}`;
    }

    async delete(entityId) {
        if (confirm("Are you sure you want to delete this item?")) {
            await fetch(`/api/${this.entityName}/${entityId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem('token'),
                },
            });
            this.fetchAndDisplay();
        }
    }

    async nextPage() {
        this.page += 1;
        const paginate = await this.paginate();
        const entities = paginate[this.entityName];
        if (entities.length > 0) {
            this.display(entities);
            this.disablePaginationButtons(paginate);
        } else {
            this.page -= 1;
        }
    }

    async prevPage() {
        if (this.page > 1) {
            this.page -= 1;
            const paginate = await this.paginate();
            const entities = paginate[this.entityName];
            this.display(entities);
            this.disablePaginationButtons(paginate);
        }
    }

    disablePaginationButtons(paginate) {
        if (this.page > 1) {
            this.prevPageButton.removeAttribute('disabled');
        } else {
            this.prevPageButton.setAttribute('disabled', 'disabled');
        }

        if (this.page == paginate.total_pages) {
            this.nextPageButton.setAttribute('disabled', 'disabled');
        } else {
            this.nextPageButton.removeAttribute('disabled');
        }
    }
}

export { EntityCRUD };
