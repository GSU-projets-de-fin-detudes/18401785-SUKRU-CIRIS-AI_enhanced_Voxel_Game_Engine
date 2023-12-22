#pragma once
#include "../core/core.h"
#include "player.h"

typedef struct chunk_op
{
  DA *chunkinfo;
  DA *batch;
  unsigned int chunk_size;
  unsigned int chunk_range;
  player *p;
  int **hm;
  int dimensionx, dimensionz;
  int previous_chunkid;
  int chunknumberinrow;
  int renderedchunkcount;
} chunk_op;

typedef struct chunk_info
{
  vec2 minxy, maxxy;
  int startx, startz;
} chunk_info;

chunk_op *create_chunk_op(unsigned int chunk_size, unsigned int chunk_range, player *p, int **hm, int dimensionx, int dimensionz);

void delete_chunk_op(chunk_op *c);

void update_chunk_op(chunk_op *c);

void use_chunk_op(chunk_op *c, GLuint program);