import bpy
import requests
import os

bl_info = {
    "name": "Google AI Studio Script Executor",
    "blender": (3, 0, 0),
    "category": "Object",
    "description": "Generate Python scripts using Google Generative Language API and execute them in Blender",
    "author": "Your Name",
    "version": (1, 2, 0),
}

API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

PROMPT_DIRECTIVE = (
    "Please respond to all prompts in ONLY valid Blender Python code, without backticks surrounding it. "
    "Any explanation or reasoning you want to make should be done in code comments following python syntax, e.g. # explanation here. "
    "This code will be run inside of a Blender scene to make changes as described by the user so it must be able to be run by the python interpreter."
    "Remember to name all of the objects you create so you can access them later."
    "The following is an example of an appropriate response given the prompt. USER: 'Add a red light above the scene'"
    "ASSISTANT: '# Sure, here is the code that will add a red light above the scene:"
    "import bpy"

    "# Create a new point light"
    "light_data = bpy.data.lights.new(name='Red_Light', type='POINT')"
    "light_object = bpy.data.objects.new(name='Red_Light', object_data=light_data)"

    "# Link the light object to the scene"
    "bpy.context.collection.objects.link(light_object)"

    "# Position the light above the scene"
    "light_object.location = (0, 0, 10)  # Adjust coordinates as needed"

    "# Set the light color to red"
    "light_data.color = (1, 0, 0)  # RGB for red"

    "# Adjust the light's energy (brightness)"
    "light_data.energy = 1000  # Adjust as needed"

    "# Make the light active"
    "bpy.context.view_layer.objects.active = light_object'"
    "================="
    "You are now to respond only as prompted by the user, in valid python code. Good luck!"
    "================="
)

AVAILABLE_MODELS = [
    "gemini-2.0-flash-thinking-exp-1219",
    "gemini-2.0-flash-exp",
    "gemini-exp-1206",
    "learnlm-1.5-pro-experimental",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
]

class GoogleAIStudioPanel(bpy.types.Panel):
    """Creates a Panel in the 3D View for text input"""
    bl_label = "Google AI Studio Script Executor"
    bl_idname = "VIEW3D_PT_google_ai_studio"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI Studio'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "ai_api_key")
        layout.prop(scene, "ai_model")
        layout.prop(scene, "ai_input_text")
        layout.operator("object.execute_generated_script", text="Generate and Execute Script")
        layout.operator("object.clear_context", text="Clear Context")

class ExecuteGeneratedScriptOperator(bpy.types.Operator):
    """Generate and execute a Python script in Blender"""
    bl_idname = "object.execute_generated_script"
    bl_label = "Generate and Execute Script"

    context_history = []  # Store conversation history in chat-style format

    def execute(self, context):
        user_input = context.scene.ai_input_text
        api_key = context.scene.ai_api_key or os.getenv("GOOGLE_AI_STUDIO_API_KEY")
        selected_model = context.scene.ai_model

        if not user_input:
            self.report({'WARNING'}, "Input text is empty")
            return {'CANCELLED'}

        if not api_key:
            self.report({'ERROR'}, "API key not provided. Set it in the panel or as an environment variable.")
            return {'CANCELLED'}

        try:
            # Add the user's input to the conversation history
            self.context_history.append({
                "role": "user",
                "parts": [{"text": user_input}]
            })

            # Construct the API request payload
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": PROMPT_DIRECTIVE}]
                    }
                ] + self.context_history  # Include the directive and history
            }

            # Construct the API URL
            api_url = API_URL_TEMPLATE.format(model=selected_model, api_key=api_key)

            # Call the API
            response = requests.post(
                api_url,
                headers={"Content-Type": "application/json"},
                json=payload
            )
            response.raise_for_status()
            api_data = response.json()

            # Debugging: Log the raw API response
            print("API Response:", api_data)

            # Extract the generated Python code
            candidates = api_data.get("candidates", [])
            if not candidates or not candidates[0].get("content"):
                self.report({'WARNING'}, "Unexpected response format or no content in response")
                return {'CANCELLED'}

            content = candidates[0]["content"]
            parts = content.get("parts", [])
            if not parts or not parts[0].get("text"):
                self.report({'WARNING'}, "No valid code found in response")
                return {'CANCELLED'}

            generated_code = parts[0]["text"]
            if not generated_code.strip():
                self.report({'WARNING'}, "Generated code is empty")
                return {'CANCELLED'}
            
            self.report({'WARNING'}, generated_code)

            # Add the model's response to the conversation history
            self.context_history.append({
                "role": "model",
                "parts": [{"text": generated_code}]
            })

            # Execute the generated Python code
            exec(generated_code, globals(), locals())
            self.report({'INFO'}, "Script executed successfully")
        except requests.exceptions.RequestException as e:
            self.report({'ERROR'}, f"API request failed: {e}")
            return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error executing the script: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}

class ClearContextOperator(bpy.types.Operator):
    """Clear the AI context history"""
    bl_idname = "object.clear_context"
    bl_label = "Clear Context"

    def execute(self, context):
        ExecuteGeneratedScriptOperator.context_history.clear()
        self.report({'INFO'}, "Context cleared")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(GoogleAIStudioPanel)
    bpy.utils.register_class(ExecuteGeneratedScriptOperator)
    bpy.utils.register_class(ClearContextOperator)
    bpy.types.Scene.ai_input_text = bpy.props.StringProperty(
        name="Input Text",
        description="Enter a description for the script",
        default=""
    )
    bpy.types.Scene.ai_api_key = bpy.props.StringProperty(
        name="API Key",
        description="Enter your Google API key",
        default=""
    )
    bpy.types.Scene.ai_model = bpy.props.EnumProperty(
        name="AI Model",
        description="Select the AI model to use",
        items=[(model, model, "") for model in AVAILABLE_MODELS],
        default="gemini-1.5-flash"
    )

def unregister():
    bpy.utils.unregister_class(GoogleAIStudioPanel)
    bpy.utils.unregister_class(ExecuteGeneratedScriptOperator)
    bpy.utils.unregister_class(ClearContextOperator)
    del bpy.types.Scene.ai_input_text
    del bpy.types.Scene.ai_api_key
    del bpy.types.Scene.ai_model

if __name__ == "__main__":
    register()
