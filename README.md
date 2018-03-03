## Build libSCOTCH 6.0.4

```
sudo apt-get install bison libbison-dev flex

# Download and unpack
mkdir scotch/
cd scotch/
wget http://gforge.inria.fr/frs/download.php/latestfile/298/scotch_6.0.4.tar.gz
tar -xvzf scotch_6.0.4.tar.gz
cd scotch_6.0.4/src/

# Creating the "Makefile.inc" file - see INSTALL.txt
ln -s Make.inc/Makefile.inc.i686_pc_linux2.shlib.debug Makefile.inc

# Build the library
cd libscotch
make VERSION=6 RELEASE=0 PATCHLEVEL=4 libscotcherr.so
sudo cp libscotcherr.so /usr/local/lib/
make VERSION=6 RELEASE=0 PATCHLEVEL=4 libscotch.so
sudo cp libscotch.so /usr/local/lib/

export LD_LIBRARY_PATH=/lib:/usr/lib:/usr/local/lib

```

## Build SCOTCH

```
cd scotch_6.0.4/src/
make scotch
```

# add -lscotcherr to the end of libscotch/Makefile so it looks like this
libscotch$(LIB)         :   $(LIBSCOTCHDEPS)
                    $(AR) $(ARFLAGS) $(@) $(?) -lscotcherr
                    -$(RANLIB) $(@)

gcc -shared -o libscotch.so arch.o arch_build.o arch_cmplt.o arch_cmpltw.o arch_deco.o arch_dist.o arch_hcub.o arch_mesh.o arch_tleaf.o arch_torus.o arch_vcmplt.o arch_vhcub.o bgraph.o bgraph_bipart_bd.o bgraph_bipart_df.o bgraph_bipart_ex.o bgraph_bipart_fm.o bgraph_bipart_gg.o bgraph_bipart_gp.o bgraph_bipart_ml.o bgraph_bipart_st.o bgraph_bipart_zr.o bgraph_check.o bgraph_store.o common.o common_file.o common_file_compress.o common_file_uncompress.o common_integer.o common_memory.o common_string.o common_stub.o common_thread.o fibo.o gain.o geom.o graph.o graph_base.o graph_band.o graph_check.o graph_coarsen.o graph_induce.o graph_io.o graph_io_chac.o graph_io_habo.o graph_io_mmkt.o graph_io_scot.o graph_list.o graph_match.o hall_order_hd.o hall_order_hf.o hall_order_hx.o hgraph.o hgraph_check.o hgraph_induce.o hgraph_order_bl.o hgraph_order_cp.o hgraph_order_gp.o hgraph_order_hd.o hgraph_order_hf.o hgraph_order_hx.o hgraph_order_kp.o hgraph_order_nd.o hgraph_order_si.o hgraph_order_st.o hmesh.o hmesh_check.o hmesh_hgraph.o hmesh_induce.o hmesh_mesh.o hmesh_order_bl.o hmesh_order_cp.o hmesh_order_gr.o hmesh_order_gp.o hmesh_order_hd.o hmesh_order_hf.o hmesh_order_hx.o hmesh_order_nd.o hmesh_order_si.o hmesh_order_st.o kgraph.o kgraph_band.o kgraph_check.o kgraph_map_bd.o kgraph_map_cp.o kgraph_map_df.o kgraph_map_ex.o kgraph_map_fm.o kgraph_map_ml.o kgraph_map_rb.o kgraph_map_rb_map.o kgraph_map_rb_part.o kgraph_map_st.o kgraph_store.o library_arch.o library_arch_f.o library_arch_build.o library_arch_build_f.o library_common_f.o library_geom.o library_geom_f.o library_graph.o library_graph_f.o library_graph_base.o library_graph_base_f.o library_graph_check.o library_graph_check_f.o library_graph_coarsen.o library_graph_coarsen_f.o library_graph_color.o library_graph_color_f.o library_graph_io_chac.o library_graph_io_chac_f.o library_graph_io_habo.o library_graph_io_habo_f.o library_graph_io_mmkt.o library_graph_io_mmkt_f.o library_graph_io_scot.o library_graph_io_scot_f.o library_graph_map.o library_graph_map_f.o library_graph_map_io.o library_graph_map_io_f.o library_graph_map_view.o library_graph_map_view_f.o library_graph_order.o library_graph_order_f.o library_graph_part_ovl.o library_graph_part_ovl_f.o library_mapping.o library_memory.o library_memory_f.o library_mesh.o library_mesh_f.o library_mesh_graph.o library_mesh_graph_f.o library_mesh_io_habo.o library_mesh_io_habo_f.o library_mesh_io_scot.o library_mesh_io_scot_f.o library_mesh_order.o library_mesh_order_f.o library_order.o library_parser.o library_parser_f.o library_random.o library_random_f.o library_strat.o library_version.o library_version_f.o mapping.o mapping_io.o mesh.o mesh_check.o mesh_coarsen.o mesh_graph.o mesh_induce_sepa.o mesh_io.o mesh_io_habo.o mesh_io_scot.o order.o order_check.o order_io.o parser.o parser_ll.o parser_yy.o vgraph.o vgraph_check.o vgraph_separate_bd.o vgraph_separate_df.o vgraph_separate_es.o vgraph_separate_fm.o vgraph_separate_gg.o vgraph_separate_gp.o vgraph_separate_ml.o vgraph_separate_st.o vgraph_separate_th.o vgraph_separate_vw.o vgraph_separate_zr.o vgraph_store.o vmesh.o vmesh_check.o vmesh_separate_fm.o vmesh_separate_gg.o vmesh_separate_gr.o vmesh_separate_ml.o vmesh_separate_zr.o vmesh_separate_st.o vmesh_store.o wgraph.o wgraph_check.o wgraph_part_fm.o wgraph_part_gg.o wgraph_part_gp.o wgraph_part_ml.o wgraph_part_rb.o wgraph_part_st.o wgraph_part_zr.o wgraph_store.o -lscotcherr 
```

