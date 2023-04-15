import { EntityCRUD } from './entity_crud.js';

class ActorCRUD extends EntityCRUD {
  constructor() {
    super('actors', 'actor-form', 'actor-list', 'prev-actor-page', 'next-actor-page');
  }

  display(actors) {
    if (!this.list) return;

    this.list.innerHTML = '<tr></tr><th>Name</th><th>Bio</th><th>Actions</th></tr>';
    this.list.innerHTML += actors.map((actor) => `
        <tr>
          <td>${actor.name}</td>
          <td>${actor.bio}</td>
          <td>
            <button class="btn btn-sm btn-warning" onclick="crudInstance.edit(${actor.id})">Edit</button>
            <button class="btn btn-sm btn-danger" onclick="crudInstance.delete(${actor.id})">Delete</button>
          </td>
        </tr>
      `).join('');
  }

  getFormData() {
    return {
      name: document.getElementById('name').value,
      bio: document.getElementById('bio').value
    };
  }
}

export { ActorCRUD };
