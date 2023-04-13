class ActorCRUD extends EntityCRUD {
    constructor() {
      super('actors', 'actor-form', 'actor-list', 'prev-actor-page', 'next-actor-page');
    }
  
    display(actors) {
      this.list.innerHTML = actors.map((actor) => `
        <tr>
          <td>${actor.name}</td>
          <td>${actor.bio}</td>
          <td>
            <button onclick="actorCRUD.update(${actor.id}, /* updatedData */)">Update</button>
            <button onclick="actorCRUD.delete(${actor.id})">Delete</button>
          </td>
        </tr>
      `).join('');
    }
  
    getFormData() {
      return {
        name: document.getElementById('actor-name').value,
        bio: document.getElementById('actor-bio').value
      };
    }
  }
  