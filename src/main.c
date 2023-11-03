#include "./core/core.h"
#include <time.h>
#include "./game/world.h"

int main(void)
{
	GLFWwindow *window = create_window(1920, 1080, 1, 1);
	if (window == 0)
	{
		return -1;
	}

	init_programs();
	camera *cam = create_camera(1920, 1080, (vec3){0.0f, 5, 0.0f}, 60, 0.1f, 200, 1, 100, -15, (vec3){1, 0, 0});
	lighting *light = create_lighting(window, cam, 8096, 8096, 0.5f);

	srand((unsigned int)time(0));
	int **hm = create_heightmap(200, 200, 4, rand(), rand());
	world *world_cubes = create_world(hm, 200, 200);
	free(hm);
	clock_t timer = 0;
	while (!glfwWindowShouldClose(window))
	{
		timer = clock();
		glfwPollEvents();
		run_input_free_camera(cam, window);

		glUseProgram(get_def_shadowmap_br_program());
		use_lighting(light, get_def_shadowmap_br_program(), 1);
		use_world(world_cubes, get_def_shadowmap_br_program());

		glUseProgram(get_def_tex_light_br_program());
		use_lighting(light, get_def_tex_light_br_program(), 0);
		use_camera(cam, get_def_tex_light_br_program());
		use_world(world_cubes, get_def_tex_light_br_program());

		glfwSwapBuffers(window);

		// simulate_physic((vec3){0, -9.8f, 0}, 0.01f);
		while ((clock() / (CLOCKS_PER_SEC / 1000)) - (timer / (CLOCKS_PER_SEC / 1000)) < 16)
			;
	}

	delete_camera(cam);
	delete_world(world_cubes);
	delete_lighting(light);

	delete_all_object();
	delete_all_physic();
	destroy_programs();
	delete_window(window);

	return 0;
}