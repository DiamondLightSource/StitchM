

def edge_definer(pixel_positions, boundaries, pixels_to_edge):
    position_on_mosaic = [pixel_positions[0] - boundaries[0, 0],
                          pixel_positions[1] - boundaries[0, 1]]
    start = (position_on_mosaic[0] - pixels_to_edge[0],
             position_on_mosaic[1] - pixels_to_edge[1])
    end = (position_on_mosaic[0] + pixels_to_edge[0],
           position_on_mosaic[1] + pixels_to_edge[1])
    return start, end
