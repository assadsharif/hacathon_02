{{/*
Expand the name of the chart.
*/}}
{{- define "todo-chatbot.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "todo-chatbot.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "todo-chatbot.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-chatbot.labels" -}}
helm.sh/chart: {{ include "todo-chatbot.chart" . }}
{{ include "todo-chatbot.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "todo-chatbot.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-chatbot.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Backend name
*/}}
{{- define "todo-chatbot.backend.name" -}}
{{- printf "%s-%s" (include "todo-chatbot.fullname" .) .Values.backend.name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Backend labels
*/}}
{{- define "todo-chatbot.backend.labels" -}}
{{ include "todo-chatbot.labels" . }}
app.kubernetes.io/component: backend
{{- end }}

{{/*
Backend selector labels
*/}}
{{- define "todo-chatbot.backend.selectorLabels" -}}
{{ include "todo-chatbot.selectorLabels" . }}
app.kubernetes.io/component: backend
{{- end }}

{{/*
Frontend name
*/}}
{{- define "todo-chatbot.frontend.name" -}}
{{- printf "%s-%s" (include "todo-chatbot.fullname" .) .Values.frontend.name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Frontend labels
*/}}
{{- define "todo-chatbot.frontend.labels" -}}
{{ include "todo-chatbot.labels" . }}
app.kubernetes.io/component: frontend
{{- end }}

{{/*
Frontend selector labels
*/}}
{{- define "todo-chatbot.frontend.selectorLabels" -}}
{{ include "todo-chatbot.selectorLabels" . }}
app.kubernetes.io/component: frontend
{{- end }}

{{/*
Database name
*/}}
{{- define "todo-chatbot.database.name" -}}
{{- printf "%s-%s" (include "todo-chatbot.fullname" .) .Values.database.name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Database labels
*/}}
{{- define "todo-chatbot.database.labels" -}}
{{ include "todo-chatbot.labels" . }}
app.kubernetes.io/component: database
{{- end }}

{{/*
Database selector labels
*/}}
{{- define "todo-chatbot.database.selectorLabels" -}}
{{ include "todo-chatbot.selectorLabels" . }}
app.kubernetes.io/component: database
{{- end }}

{{/*
Database URL helper - constructs the PostgreSQL connection string
*/}}
{{- define "todo-chatbot.databaseUrl" -}}
{{- if .Values.secrets.databaseUrl }}
{{- .Values.secrets.databaseUrl }}
{{- else }}
{{- printf "postgresql://%s:%s@%s:%d/%s" .Values.database.credentials.username .Values.database.credentials.password (include "todo-chatbot.database.name" .) (int .Values.database.service.port) .Values.database.credentials.database }}
{{- end }}
{{- end }}

{{/*
Secret name
*/}}
{{- define "todo-chatbot.secret.name" -}}
{{- printf "%s-secrets" (include "todo-chatbot.fullname" .) }}
{{- end }}
