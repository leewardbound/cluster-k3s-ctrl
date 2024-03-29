{{- define "penpot.ingress.isStable" -}}
  {{- $isStable := "" -}}
  {{- if eq (include "common.capabilities.ingress.apiVersion" $) "networking.k8s.io/v1" -}}
    {{- $isStable = "true" -}}
  {{- end -}}
  {{- $isStable -}}
{{- end -}}

{{- define "penpot.env" -}}
  {{- range $k, $v := .values -}}
    {{- if kindIs "map" $v -}}
      {{- range $sk, $sv := $v -}}
        {{- include "penpot.env" (dict "root" $.root "values" (dict (printf "%s__%s" (upper $k) (upper $sk)) $sv)) -}}
      {{- end -}}
    {{- else -}}
      {{- $value := $v -}}
      {{- if or (kindIs "bool" $v) (kindIs "float64" $v) -}}
        {{- $v = quote $v -}}
      {{- else -}}
        {{- $v = tpl $v $.root | quote }}
      {{- end -}}
      {{- if and ($v) (ne $v "\"\"") }}
- name: {{ printf "PENPOT_%s" (upper $k) }}
  value: {{ $v }}
      {{- end }}
    {{- end -}}
  {{- end -}}
{{- end -}}
