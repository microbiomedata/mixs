# document installation of poetry application and `poetry install`

RUN=poetry run

.PHONY: all clean gh_docs docserve

# html_docs
all: clean generated/mixs.py mkdocs_html/index.html

# ---------------------------------------
# TSVs from google drive
# ---------------------------------------
# for seeding

clean:
	#rm -rf downloads/*tsv
	rm -rf generated/*
	rm -rf logs/*
	rm -rf mkdocs_html/
	#rm -rf model/schema/*yaml

#model/schema/mixs.yaml: downloads/mixs6.tsv downloads/mixs6_core.tsv
#	$(RUN) python -m gsctools.mixs_converter  2>&1 | tee -a logs/sheet2linkml.log

downloads/gsc_mixs6.tsv:
	curl -L -s 'https://docs.google.com/spreadsheets/d/1QDeeUcDqXes69Y2RjU2aWgOpCVWo5OVsBX9MKmMqi_o/export?format=tsv&gid=750683809' > $@
downloads/gsc_mixs6.csv:
	curl -L -s 'https://docs.google.com/spreadsheets/d/1QDeeUcDqXes69Y2RjU2aWgOpCVWo5OVsBX9MKmMqi_o/export?format=csv&gid=750683809' > $@
downloads/gsc_mixs6_core.tsv:
	curl -L -s 'https://docs.google.com/spreadsheets/d/1QDeeUcDqXes69Y2RjU2aWgOpCVWo5OVsBX9MKmMqi_o/export?format=tsv&gid=178015749' > $@

# GSC: MIxS 6 term updates:MIxS6 Core- Final_clean
#   https://docs.google.com/spreadsheets/d/1QDeeUcDqXes69Y2RjU2aWgOpCVWo5OVsBX9MKmMqi_o/edit#gid=178015749
# GSC: MIxS 6 term updates:MIxS6 packages - Final_clean
#   https://docs.google.com/spreadsheets/d/1QDeeUcDqXes69Y2RjU2aWgOpCVWo5OVsBX9MKmMqi_o/edit#gid=750683809

# NMDC: NMDC copy of MIxS 6 term updates:
#   https://docs.google.com/spreadsheets/d/1-ocpwjx6nkBod6aj4kcYeSB5NRlhXaYCcuk3ooX2OV4/edit#gid=178015749
# NMDC MIxS 6 term updates:MIxS6 packages - Final_clean
#   https://docs.google.com/spreadsheets/d/1-ocpwjx6nkBod6aj4kcYeSB5NRlhXaYCcuk3ooX2OV4/edit#gid=750683809

downloads/nmdc_mixs6.tsv:
	curl -L -s 'https://docs.google.com/spreadsheets/d/1-ocpwjx6nkBod6aj4kcYeSB5NRlhXaYCcuk3ooX2OV4/export?format=tsv&gid=750683809' > $@
downloads/nmdc_mixs6.csv:
	curl -L -s 'https://docs.google.com/spreadsheets/d/1-ocpwjx6nkBod6aj4kcYeSB5NRlhXaYCcuk3ooX2OV4/export?format=csv&gid=750683809' > $@
downloads/nmdc_mixs6_extracol.csv: downloads/nmdc_mixs6.csv
	# csvdiff: command failed - base-file and delta-file columns count do not match
	poetry run python util/blank_col_for_csv.py \
		--csv_in $< \
		--csv_out $@ \
		--col_name removed
downloads/nmdc_mixs6_core.tsv:
	curl -L -s 'https://docs.google.com/spreadsheets/d/1-ocpwjx6nkBod6aj4kcYeSB5NRlhXaYCcuk3ooX2OV4/export?format=tsv&gid=178015749' > $@

.PHONY: gsc_vs_nmdc clean_diff_stuff

clean_diff_stuff:
	rm -rf downloads/*sv

gsc_vs_nmdc: downloads/gsc_mixs6.csv downloads/nmdc_mixs6_extracol.csv
	csvdiff \
		--primary-key 0,1 \
		--format word-diff $^
# --format string         Available (rowmark|json|legacy-json|diff|word-diff|color-words) (default "diff")

# todo add owl back in and make it awesome
# todo derive output path from target file name
# 		--exclude owl \

generated/mixs.py: model/schema/mixs.yaml
	$(RUN) gen-project \
		--exclude excel \
		--exclude java \
		--exclude markdown \
		--dir $(dir $@) $< 2>&1 | tee -a logs/linkml_artifact_generation.log
#	mkdir generated/excel
#	$(RUN) gen-excel --output generated/excel/mixs.xlsx $<
#	# skipping jinja --template_file
#	mkdir generated/java
#	$(RUN) gen-java --package mixs --output_directory generated/java $<

## ---------------------------------------
## MARKDOWN DOCS
##      Generate documentation ready for mkdocs
## ---------------------------------------
## For help with mkdocs see https://www.mkdocs.org/.

generated/docs/index.md: model/schema/mixs.yaml generated/mixs.py
	$(RUN) gen-doc $< --directory $(dir $@) --template-directory doc_templates

generated/docs/introduction/%.md: generated/docs/index.md
	cp -R static_md/* $(dir $@)

# add more logging?
# some docs pages not being created
# usage of mkdocs.yml attributes like analytics?

mkdocs_html/index.html: generated/docs/index.md
	poetry run mkdocs build

# test docs locally.
# repeats build
docserve:
	$(RUN) mkdocs serve

# repeats build
# pushes to gh-pages branch
# exposes at https://GenomicsStandardsConsortium.github.io/mixs/
gh_docs:
	poetry run mkdocs gh-deploy
