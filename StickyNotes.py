from typing import Any, override
from .NotesStore import NotesStore
from lib.PluginHelper import PluginHelper, PluginManifest
from lib.PluginSettingDefinitions import PluginSettings, SettingsGrid, ParagraphSetting
from lib.Logger import log
from lib.PluginBase import PluginBase
import os

# Main plugin class
# This is the class that will be loaded by the PluginManager.
class StickyNotes(PluginBase):
    def __init__(self, plugin_manifest: PluginManifest):
        super().__init__(plugin_manifest)

        self._notes_store: NotesStore  | None = None

        # Define the plugin settings
        # This is the settings that will be shown in the UI for this plugin.
        self.settings_config: PluginSettings | None = PluginSettings(
            key="StickyNotesPlugin",
            label="Sticky Notes",
            icon="note_stack", # Uses Material Icons, like the built-in settings-tabs.
            grids=[
                SettingsGrid(
                    key="general",
                    label="General",
                    fields=[
                        ParagraphSetting(
                            key="is_active",
                            label="Sticky Notes is active.",
                            type="paragraph",
                            readonly=False,
                            placeholder=None,
                            content="Sticky Notes appears to be active. You can create, update, and delete notes.",
                        ),
                    ]
                ),
            ]
        )
    
    @override
    def register_actions(self, helper: PluginHelper):
        # Register actions
        helper.register_action('sticky_notes_update_note', "Adds or updates a note.", {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "The ID of the note to update. If not provided, a new note will be created."
                },
                "content": {
                    "type": "string",
                    "description": "The content of the note."
                }
            }
        }, self.sticky_notes_update_note, 'global')

        helper.register_action('sticky_notes_get_notes', "Gets all notes.", {
            "type": "object",
            "properties": {}
        }, self.sticky_notes_get_notes, 'global')

        helper.register_action('sticky_notes_delete_note', "Deletes a note.", {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "The ID of the note to delete."
                }
            }
        }, self.sticky_notes_delete_note, 'global')

        log('debug', f"Actions registered for {self.plugin_manifest.name}")
        
    @override
    def register_projections(self, helper: PluginHelper):
        # Register projections
        pass

    @override
    def register_sideeffects(self, helper: PluginHelper):
        # Register side effects
        pass
        
    @override
    def register_prompt_event_handlers(self, helper: PluginHelper):
        # Register prompt generators
        pass
        
    @override
    def register_status_generators(self, helper: PluginHelper):
        # Register prompt generators
        helper.register_status_generator(self.all_notes_status_generator)

    @override
    def register_should_reply_handlers(self, helper: PluginHelper):
        # Register should_reply handlers
        pass
    
    @override
    def on_plugin_helper_ready(self, helper: PluginHelper):
        # Executed when the plugin helper is ready

        # Here we initialize the database, in case it doesn't exist yet.
        db_path = os.path.join(helper.get_plugin_data_path(self.plugin_manifest), "sticky_notes.db")
        self._notes_store = NotesStore(db_path)
        self._notes_store.initialize_db()
        log('debug', f"Database initialized at {db_path}")
    
    @override
    def on_chat_stop(self, helper: PluginHelper):
        # Executed when the chat is stopped
        pass

    # Actions
    def sticky_notes_update_note(self, args, projected_states) -> str:
        if 'content' not in args:
            return "Content is required to create or update a note."

        if self._notes_store is None:
            return "Store is not initialized. Please initialize the plugin first."

        if 'id' in args:
            # Update existing note
            if self._notes_store.update_note(args['id'], args['content']):
                return f"Note with ID {args['id']} updated."
            return f"Note with ID {args['id']} not found."
        else:
            # Create new note
            new_note_id = self._notes_store.add_note(args['content'])
            if new_note_id is None:
                return "Failed to create a new note."
            return f"New note created with ID {new_note_id}."
    
    def sticky_notes_get_notes(self, args, projected_states) -> str:
        if self._notes_store is None:
            return "Store is not initialized. Please initialize the plugin first."

        return str(self._notes_store.get_notes())
    
    def sticky_notes_delete_note(self, args, projected_states) -> str:
        if 'id' not in args:
            return "ID is required to delete a note."

        if self._notes_store is None:
            return "Store is not initialized. Please initialize the plugin first."
        
        if self._notes_store.delete_note(args['id']):
            return f"Note with ID {args['id']} deleted."
        
        return f"Note with ID {args['id']} not found."

    def all_notes_status_generator(self, projected_states: dict[str, dict]) -> list[tuple[str, Any]]:
        ret_val = []
        if self._notes_store is not None:
            ret_val = self._notes_store.get_notes() # Database path is not set. Please initialize the plugin first.
        return [
            ('All notes', ret_val)
        ]
